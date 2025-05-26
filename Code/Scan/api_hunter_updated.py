from config import ALIVE_SUBS, FFUF, NUCLEI, COMMON_WORDLIST
from pathlib import Path
import subprocess
import requests
import os

# === KIỂM TRA FILE INPUT ===
if not ALIVE_SUBS.exists() or ALIVE_SUBS.stat().st_size == 0:
    print("⚠️ Không có domain hoạt động để quét API.")
    exit()

# === CẤU HÌNH ===
OUTPUT_DIR = Path("D:/results/api_hunt")
httpx_targets = OUTPUT_DIR / "httpx_targets.txt"
api_summary = OUTPUT_DIR / "api_scan_summary.txt"
fuzz_result = OUTPUT_DIR / "api_fuzz_results.json"
nuclei_result = OUTPUT_DIR / "api_vuln_results.txt"

API_PATHS = [
    "/api", "/api/v1", "/api/v1/users", "/graphql",
    "/swagger.json", "/openapi.json"
]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === STEP 1: Chuẩn hóa URL từ subdomain ===
with ALIVE_SUBS.open("r") as f:
    urls = [f"https://{line.strip()}"]()
