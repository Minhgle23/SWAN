import subprocess
import os
import sys
from config import SUBFINDER, AMASS, DNSX, ALL_SUBS, ALIVE_SUBS
from pathlib import Path

def ensure_file_exists(*paths):
    for path in paths:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).touch(exist_ok=True)

ensure_file_exists(ALL_SUBS, ALIVE_SUBS)

# ========== SUBDOMAIN ENUM ==========

def run_subfinder(domain):
    print("[*] Đang chạy subfinder...")
    try:
        result = subprocess.run(
            [str(SUBFINDER), "-d", domain, "-silent"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print("[-] Lỗi subfinder:", e)
        return []


def run_amass(domain):
    print("[*] Đang chạy amass...")
    try:
        result = subprocess.run(
            [str(AMASS), "enum", "-passive", "-d", domain],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print("[-] Lỗi amass:", e)
        return []


# ========== ALIVE CHECK ==========

def check_alive(subdomains):
    print("[*] Kiểm tra subdomain sống (dnsx)...")
    try:
        result = subprocess.run(
            [str(DNSX), "-silent"],
            input="\n".join(subdomains),
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print("[-] Lỗi dnsx:", e)
        return []


# ========== LƯU FILE ==========

def save_to_file(lines, filepath):
    try:
        os.makedirs(filepath.parent, exist_ok=True)
        with filepath.open("w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"[✓] Đã lưu {len(lines)} dòng vào: {filepath}")
    except Exception as e:
        print(f"[-] Lỗi khi ghi file: {e}")


# ========== MAIN ==========

def main():
    # Ưu tiên lấy từ sys.argv nếu có
    if len(sys.argv) > 1:
        domain = sys.argv[1].strip()
    else:
        domain = input("Nhập domain (ví dụ: example.com): ").strip()

    if not domain:
        print("⚠️ Không có domain.")
        return

    # Bắt đầu quét
    subs1 = run_subfinder(domain)
    subs2 = run_amass(domain)
    all_subs = sorted(set(subs1 + subs2))

    print(f"[+] Tổng cộng {len(all_subs)} subdomain (sau khi loại trùng).")
    save_to_file(all_subs, ALL_SUBS)

    if all_subs:
        alive_subs = check_alive(all_subs)
        save_to_file(alive_subs or [domain], ALIVE_SUBS)
    else:
        alive_subs = []
        save_to_file([domain], ALIVE_SUBS)

    print("\n========== KẾT QUẢ ==========")
    if alive_subs:
        for sub in alive_subs:
            print(sub)
        print(f"\nTổng cộng: {len(alive_subs)} / {len(all_subs)} subdomain đang hoạt động.")
    else:
        print("Không có subdomain hoạt động. Ghi domain:", domain)


if __name__ == "__main__":
    main()
