import sqlite3
from pathlib import Path

# === Đường dẫn chính xác đến file .txt ===
DB_PATH = "D:/results/subdomain_DB.db"                # Đặt phần mở rộng .db cho đúng chuẩn
ALL_FILE = Path("D:/results/all_subs.txt")
ALIVE_FILE = Path("D:/results/alive_subs.txt")

def read_domains(file_path):
    if not file_path.exists():
        print(f"[!] Không tìm thấy file: {file_path}")
        return set()
    with file_path.open("r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS domain_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            activity BOOLEAN NOT NULL CHECK (activity IN (0, 1)),
            added_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def save_status_to_db(all_domains, alive_domains):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for domain in sorted(all_domains):
        is_alive = 1 if domain in alive_domains else 0
        c.execute("INSERT INTO domain_status (domain, activity) VALUES (?, ?)", (domain, is_alive))

    conn.commit()
    conn.close()
    print(f"[✓] Đã lưu {len(all_domains)} domain vào database.")

def main():
    init_db()
    all_domains = read_domains(ALL_FILE)
    alive_domains = read_domains(ALIVE_FILE)
    save_status_to_db(all_domains, alive_domains)

if __name__ == "__main__":
    main()
