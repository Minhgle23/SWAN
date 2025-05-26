import os
import subprocess
from config import ALIVE_SUBS, HTTPX, KATANA, FFUF, COMMON_WORDLIST


# Đường dẫn đến file chứa IP đã resolve
INPUT_FILE = "D:/results/Resolve_IP.txt"
# Thư mục xuất kết quả port scan
OUTPUT_DIR = "D:/results/portscan"
# Đường dẫn đầy đủ đến nmap.exe
NMAP_PATH = r"C:\Program Files (x86)\nmap\nmap.exe"

def extract_ips(file_path):
    """Trích xuất các IP từ file resolve, bỏ qua các dòng CNAME"""
    ips = set()
    with open(file_path, "r") as f:
        for line in f:
            if " A " in line:
                parts = line.strip().split()
                if parts[-2] == "A":
                    ips.add(parts[-1])
    return sorted(ips)

def run_nmap_scan(ip, output_dir):
    """Chạy nmap với script mặc định và lưu output"""
    output_file = os.path.join(output_dir, f"{ip.replace('.', '_')}.txt")
    command = [
        NMAP_PATH,
        "-sV",           # Scan version dịch vụ
        "-Pn",           # Bỏ qua ping
        "-T4",           # Tốc độ quét nhanh
        "--script=default", # Dùng script mặc định
        "-oN", output_file, # Output dạng text
        ip
    ]
    print(f"[+] Scanning {ip} ...")
    subprocess.run(command)

def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Không tìm thấy file đầu vào: {INPUT_FILE}")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    ip_list = extract_ips(INPUT_FILE)
    print(f"[+] Đã lấy {len(ip_list)} IP để scan")

    for ip in ip_list:
        run_nmap_scan(ip, OUTPUT_DIR)

if __name__ == "__main__":
    main()
