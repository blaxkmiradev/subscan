# SubScan — Subdomain Enumerator

A simple, fast subdomain enumerator written in Python. Uses a wordlist + multithreaded DNS resolution to find live subdomains and saves results to a `.txt` file.

No external libraries required — runs on Python standard library only.

---

## Requirements

- Python 3.6+
- A wordlist file (see below)

---

## Usage

```bash
python subscan.py <domain> <wordlist> [threads]
```

| Argument | Required | Description |
|---|---|---|
| `domain` | ✅ | Target domain (e.g. `example.com`) |
| `wordlist` | ✅ | Path to your wordlist file |
| `threads` | ❌ | Number of threads (default: `50`) |

### Examples

```bash
# Basic scan
python subscan.py example.com wordlist.txt

# Faster scan with 100 threads
python subscan.py example.com wordlist.txt 100
```

---

## Output

Found subdomains are printed to the terminal and **automatically saved** to a file:

```
example_com_success.txt
```

Example file content:
```
# SubScan results for example.com
# Date: 2025-03-29 14:22:01
# Found: 4

www.example.com       93.184.216.34
mail.example.com      93.184.216.11
dev.example.com       93.184.216.55
api.example.com       93.184.217.3
```

---

## Wordlists

You can use any plain `.txt` wordlist with one word per line. Recommended free sources:

- [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS) — `subdomains-top1million-5000.txt`
- [assetnote wordlists](https://wordlists.assetnote.io/)

Quick starter wordlist to create yourself:

```
www
mail
dev
api
staging
admin
test
blog
shop
vpn
```

---

## How It Works

1. Reads each word from the wordlist
2. Builds a subdomain: `word.domain.com`
3. Tries to resolve it via DNS (`socket.gethostbyname`)
4. If it resolves → prints it as found + saves to file
5. Uses `ThreadPoolExecutor` for speed

---

## ⚠️ Legal Notice

Only scan domains you own or have **explicit written permission** to test.  
Unauthorized scanning may violate computer fraud laws in your jurisdiction.

---

## License

MIT
