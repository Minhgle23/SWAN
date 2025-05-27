import sqlite3
from pathlib import Path

result_file = Path("D:/results/Resolve_IP.txt")
db_path = "D:/results/dns_results.db"

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dns_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            record_type TEXT NOT NULL,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_dns_records():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with result_file.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                domain = parts[0].rstrip(".")
                record_type = parts[1]
                value = " ".join(parts[2:]).rstrip(".")
                cursor.execute(
                    "INSERT INTO dns_records (domain, record_type, value) VALUES (?, ?, ?)",
                    (domain, record_type, value)
                )
    conn.commit()
    conn.close()
    print(" Đã lưu DNS records vào database.")

def main():
    init_db()
    save_dns_records()

if __name__ == "__main__":
    main()
