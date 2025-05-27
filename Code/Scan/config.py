from pathlib import Path

# === Gốc thư mục ===
BASE_DIR = Path("D:/")
TOOLS = BASE_DIR / "tools"
WORDLISTS = BASE_DIR / "wordlists"
RESULTS = BASE_DIR / "results"

# === Tool executables ===
SUBFINDER = TOOLS / "subfinder.exe"
AMASS = TOOLS / "amass.exe"
DNSX = TOOLS / "dnsx.exe"
HTTPX = TOOLS / "httpx.exe"
KATANA = TOOLS / "katana.exe"
FFUF = TOOLS / "ffuf.exe"
NUCLEI = TOOLS / "nuclei.exe"

# === Wordlists ===
RESOLVERS = WORDLISTS / "resolvers.txt"
COMMON_WORDLIST = WORDLISTS / "common.txt"

# === Output files ===
ALL_SUBS = RESULTS / "all_subs.txt"
ALIVE_SUBS = RESULTS / "alive_subs.txt"
RESOLVED_IP = RESULTS / "Resolve_IP.txt"

# === Web recon ===
WEB_RECON_DIR = RESULTS / "web_recon"
HTTPX_OUTPUT = WEB_RECON_DIR / "httpx_output.txt"
HTTPX_SUMMARY = WEB_RECON_DIR / "httpx_summary.txt"
KATANA_DIR = WEB_RECON_DIR / "katana"
FFUF_DIR = WEB_RECON_DIR / "ffuf"

# === API recon ===
API_HUNT_DIR = RESULTS / "api_hunt"
API_HTTPX_TARGETS = API_HUNT_DIR / "httpx_targets.txt"
API_SUMMARY = API_HUNT_DIR / "api_scan_summary.txt"
API_FUZZ_JSON = API_HUNT_DIR / "api_fuzz_results.json"
API_NUCLEI_OUT = API_HUNT_DIR / "api_vuln_results.txt"

# === Database paths (nếu muốn quy định)
SUBDOMAIN_DB = RESULTS / "subdomain_DB"
PORTSCAN_DB = RESULTS / "nmap_scan_results"
DOMAIN_STATUS = RESULTS / "domain_status"
