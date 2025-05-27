import os
import subprocess
import sqlite3
from datetime import datetime

INPUT_FILE = "D:/results/Resolve_IP.txt"
OUTPUT_DIR = "D:/results/portscan"
NMAP_PATH = r"C:\Program Files (x86)\nmap\nmap.exe"
DB_PATH = "D:/results/nmap_scan_results.db"

def extract_ips(file_path):
    ips = set()
    with open(file_path, "r") as f:
        for line in f:
            if " A " in line:
                parts = line.strip().split()
                if parts[-2] == "A":
                    ips.add(parts[-1])
    return sorted(ips)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS port_scan_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            port INTEGER,
            protocol TEXT,
            service TEXT,
            version TEXT,
            scanned_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def parse_nmap_output(file_path, ip):
    results = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("PORT"):
                continue  # bỏ header PORT   STATE   SERVICE   VERSION
            if "/" in line and ("open" in line or "open|filtered" in line):
                parts = line.strip().split()
                if len(parts) >= 3:
                    port_proto = parts[0]    # ví dụ: 80/tcp
                    port, proto = port_proto.split("/")
                    service = parts[2]
                    version = " ".join(parts[3:]) if len(parts) > 3 else ""
                    results.append((ip, int(port), proto, service, version))
    return results

def save_to_db(scan_results):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for ip, port, proto, service, version in scan_results:
        c.execute("""
            INSERT INTO port_scan_results (ip, port, protocol, service, version)
            VALUES (?, ?, ?, ?, ?)
        """, (ip, port, proto, service, version))
    conn.commit()
    conn.close()

def run_nmap_scan(ip, output_dir):
    output_file = os.path.join(output_dir, f"{ip.replace('.', '_')}.txt")
    command = [
        NMAP_PATH,
        "-sV", "-Pn", "-T4", "--script=default",
        "-oN", output_file,
        ip
    ]
    print(f"[+] Scanning {ip} ...")
    subprocess.run(command)
    return output_file

def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Không tìm thấy file đầu vào: {INPUT_FILE}")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    init_db()
    ip_list = extract_ips(INPUT_FILE)
    print(f"[+] Đã lấy {len(ip_list)} IP để scan")

    for ip in ip_list:
        result_file = run_nmap_scan(ip, OUTPUT_DIR)
        scan_data = parse_nmap_output(result_file, ip)
        save_to_db(scan_data)
        print(f"[✓] Lưu {len(scan_data)} cổng từ {ip} vào DB.")

if __name__ == "__main__":
    main()
