import sqlite3
import os
import re

# === CẤU HÌNH ===
httpx_out = "D:/results/web_recon/httpx_output.txt"
db_path = "D:/results/web_recon.db"  # <-- CHỈNH SỬA Ở ĐÂY

def init_db():
    """Tạo bảng nếu chưa tồn tại"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS httpx_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            status_code INTEGER,
            tech TEXT,
            content_type TEXT,
            title TEXT,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def parse_httpx_to_db():
    """Đọc file httpx_output.txt và lưu kết quả vào CSDL"""
    if not os.path.exists(httpx_out):
        print(f"[!] Không tìm thấy file: {httpx_out}")
        return

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(httpx_out, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" ")
            if not parts or len(parts) < 2:
                continue

            url = parts[0]
            status_raw = parts[1].strip("[]")
            status_clean = ansi_escape.sub('', status_raw)

            try:
                status_code = int(status_clean)
            except ValueError:
                status_code = None

            tech = parts[2].strip("[]") if len(parts) > 2 else ""
            content_type = parts[3].strip("[]") if len(parts) > 3 else ""
            title = " ".join(parts[4:]).replace("[title:", "").replace("]", "").strip(": ")

            c.execute("""
                INSERT INTO httpx_results (url, status_code, tech, content_type, title)
                VALUES (?, ?, ?, ?, ?)
            """, (url, status_code, tech, content_type, title))

    conn.commit()
    conn.close()
    print("[✓] Đã nhập kết quả từ file httpx vào CSDL.")

def main():
    init_db()
    parse_httpx_to_db()

if __name__ == "__main__":
    main()
