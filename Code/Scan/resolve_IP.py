import subprocess
from pathlib import Path
from config import ALIVE_SUBS, RESOLVED_IP, RESOLVERS  # dùng đúng từ config

# === LÀM SẠCH INPUT ===
def clean_domains(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        line = line.strip()
        if line.startswith("http://") or line.startswith("https://"):
            line = line.replace("https://", "").replace("http://", "")
        domain = line.split("/")[0]
        if domain:
            cleaned.append(domain)

    with file_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))

    print(f"✅ Đã chuẩn hóa {file_path.name} ({len(cleaned)} dòng)")

# === CHUẨN HÓA FILE ===
for path in [ALIVE_SUBS, RESOLVERS]:
    if not path.exists():
        raise FileNotFoundError(f"❌ Không tìm thấy file: {path}")

clean_domains(ALIVE_SUBS)

# === GỌI MASSDNS TRONG WSL ===
wsl_cmd = [
    "wsl",
    "~/massdns/bin/massdns",
    "-r", f"/mnt/d{RESOLVERS.as_posix()[2:]}",  # đổi D:/ → /mnt/d/
    "-o", "S",
    "-w", f"/mnt/d{RESOLVED_IP.as_posix()[2:]}",
    f"/mnt/d{ALIVE_SUBS.as_posix()[2:]}"
]

print("➡️ Đang chạy massdns trong WSL:")
print(" ".join(wsl_cmd))

try:
    result = subprocess.run(wsl_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"\n✅ massdns đã chạy thành công, kết quả lưu tại: {RESOLVED_IP}")
    else:
        print(f"\n❌ massdns lỗi:\n{result.stderr}")
except Exception as e:
    print(f"\n❌ Lỗi không mong muốn khi chạy massdns: {e}")
