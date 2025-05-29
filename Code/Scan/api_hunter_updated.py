from config import ALIVE_SUBS, FFUF, NUCLEI, COMMON_WORDLIST
from pathlib import Path
import subprocess
import os

def ensure_file_exists(*paths):
    for path in paths:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).touch(exist_ok=True)

# Đường dẫn đến wordlist chứa các path (endpoint)
wordlist_path = Path(r"D:\wordlists\common.txt")
ensure_file_exists(ALIVE_SUBS, COMMON_WORDLIST)



# Kiểm tra file subdomain
if not ALIVE_SUBS.exists() or ALIVE_SUBS.stat().st_size == 0:
    print("⚠️ Không có domain hoạt động để quét API.")
    exit()

# Kiểm tra file wordlist path
if not wordlist_path.exists() or wordlist_path.stat().st_size == 0:
    print(f"⚠️ File wordlist path {wordlist_path} không tồn tại hoặc rỗng.")
    exit()

# Thư mục lưu kết quả
OUTPUT_DIR = Path("D:/results/api_hunt")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

httpx_targets = OUTPUT_DIR / "httpx_targets.txt"
fuzz_result = OUTPUT_DIR / "api_fuzz_results.json"
nuclei_result = OUTPUT_DIR / "api_vuln_results.txt"

# Đọc subdomain và các đường dẫn rồi ghép URL
with ALIVE_SUBS.open("r") as f_subs, wordlist_path.open("r") as f_words:
    subs = [line.strip() for line in f_subs if line.strip()]
    paths = [line.strip() for line in f_words if line.strip()]

urls = [f"https://{sub}{path if path.startswith('/') else '/' + path}" for sub in subs for path in paths]

# Ghi các URL này vào file để dùng cho các bước sau
with httpx_targets.open("w") as f:
    for url in urls:
        f.write(url + "\n")

print(f"✅ Đã tạo danh sách URL để quét tại: {httpx_targets}")

# === Chạy ffuf quét API ===
ffuf_cmd = [
    str(FFUF),
    "-w", str(httpx_targets),
    "-u", "FUZZ",
    "-recursion",
    "-recursion-depth", "2",
    "-o", str(fuzz_result),
    "-of", "json"
]

print("🔎 Đang chạy ffuf để quét API...")
result_ffuf = subprocess.run(ffuf_cmd, capture_output=True, text=True)

if result_ffuf.returncode == 0:
    print(f"✅ ffuf quét API hoàn thành, kết quả lưu ở: {fuzz_result}")
else:
    print("❌ ffuf quét API thất bại:")
    print(result_ffuf.stderr)

# === Chạy nuclei quét lỗ hổng ===
nuclei_cmd = [
    str(NUCLEI),
    "-l", str(httpx_targets),
    "-o", str(nuclei_result)
]

print("🔎 Đang chạy nuclei để quét lỗ hổng...")
result_nuclei = subprocess.run(nuclei_cmd, capture_output=True, text=True)

if result_nuclei.returncode == 0:
    print(f"✅ nuclei quét lỗ hổng hoàn thành, kết quả lưu ở: {nuclei_result}")
else:
    print("❌ nuclei quét lỗ hổng thất bại:")
    print(result_nuclei.stderr)
