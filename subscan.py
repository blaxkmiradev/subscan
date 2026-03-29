import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ─────────────────────────────────────────
#  SubScan — Simple Subdomain Enumerator
# ─────────────────────────────────────────

BANNER = r"""
  ____        _    ____                 
 / ___| _   _| |__/ ___|  ___ __ _ _ __  
 \___ \| | | | '_ \___ \ / __/ _` | '_ \ 
  ___) | |_| | |_) |__) | (_| (_| | | | |
 |____/ \__,_|_.__/____/ \___\__,_|_| |_|

  Simple Subdomain Enumerator  |  https://github.com/blaxkmiradev/subscan
"""

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
DIM    = "\033[2m"


def resolve(subdomain):
    """Try to resolve a subdomain. Returns IP string or None."""
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except socket.gaierror:
        return None


def scan(domain, wordlist_path, threads=50, output_file=None):
    # Load wordlist
    if not os.path.isfile(wordlist_path):
        print(f"{RED}[!] Wordlist not found: {wordlist_path}{RESET}")
        sys.exit(1)

    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        words = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    total   = len(words)
    found   = []
    checked = 0

    print(f"\n{CYAN}[*] Target    : {domain}{RESET}")
    print(f"{CYAN}[*] Wordlist  : {wordlist_path} ({total} entries){RESET}")
    print(f"{CYAN}[*] Threads   : {threads}{RESET}")
    print(f"{CYAN}[*] Started   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{DIM}{'─'*55}{RESET}\n")

    start = datetime.now()

    def check(word):
        sub = f"{word}.{domain}"
        ip = resolve(sub)
        return sub, ip

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check, w): w for w in words}
        for future in as_completed(futures):
            checked += 1
            sub, ip = future.result()

            # Progress bar
            pct  = int((checked / total) * 40)
            bar  = f"[{'█'*pct}{'░'*(40-pct)}] {checked}/{total}"
            print(f"\r{DIM}{bar}{RESET}", end="", flush=True)

            if ip:
                found.append((sub, ip))
                print(f"\r{GREEN}[+] {sub:<45} {ip}{RESET}")

    elapsed = (datetime.now() - start).total_seconds()
    print(f"\n{DIM}{'─'*55}{RESET}")
    print(f"\n{CYAN}[*] Scan complete in {elapsed:.1f}s")
    print(f"[*] Checked : {checked}")
    print(f"[*] Found   : {GREEN}{len(found)}{RESET}{CYAN} subdomains{RESET}\n")

    # Save results
    if found:
        if not output_file:
            safe = domain.replace(".", "_")
            output_file = f"{safe}_success.txt"

        with open(output_file, "w") as f:
            f.write(f"# SubScan results for {domain}\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Found: {len(found)}\n\n")
            for sub, ip in found:
                f.write(f"{sub}  {ip}\n")

        print(f"{GREEN}[✓] Results saved → {output_file}{RESET}\n")
    else:
        print(f"{YELLOW}[!] No subdomains found.{RESET}\n")

    return found


def usage():
    print(f"""
{CYAN}Usage:{RESET}
  python subscan.py <domain> <wordlist> [threads]

{CYAN}Examples:{RESET}
  python subscan.py example.com wordlist.txt
  python subscan.py example.com wordlist.txt 100
""")


if __name__ == "__main__":
    print(CYAN + BANNER + RESET)

    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    domain_arg   = sys.argv[1].strip().lstrip("http://").lstrip("https://").rstrip("/")
    wordlist_arg = sys.argv[2]
    threads_arg  = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    scan(domain_arg, wordlist_arg, threads=threads_arg)
