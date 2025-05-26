from pathlib import Path

# === Gốc thư mục ===
BASE_DIR = Path("D:/")
TOOLS = BASE_DIR / "tools"
WORDLISTS = BASE_DIR / "wordlists"
RESULTS = BASE_DIR / "results"

# === Tool path ===
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
