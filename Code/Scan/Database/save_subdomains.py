import sqlite3
from pathlib import Path

# Đường dẫn file kết quả
result_file = Path("D:/results/Resolve_IP.txt")

# Kết nối DB
conn = sqlite3.connect("D:/results/dns_results.db")
cursor = conn.cursor()

# Tạo bảng nếu chưa có
cursor.execute("""
CREATE TABLE IF NOT EXISTS dns_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL,
    record_type TEXT NOT NULL,
    value TEXT NOT NULL
)
""")

# Đọc file và ghi dữ liệu
with result_file.open("r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            domain = parts[0].rstrip(".")
            record_type = parts[1]
            value = " ".join(parts[2:]).rstrip(".")
            print(f"Inserting: {domain} | {record_type} | {value}")
            cursor.execute(
                "INSERT INTO dns_records (domain, record_type, value) VALUES (?, ?, ?)",
                (domain, record_type, value)
            )

# Lưu và đóng kết nối
conn.commit()
conn.close()
print("Đã lưu dữ liệu vào database.")
# Kiểm tra lại số lượng bản ghi sau khi chèn
conn = sqlite3.connect("D:/results/dns_results.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM dns_records")
count = cursor.fetchone()[0]
print(f"Tổng số bản ghi sau khi insert: {count}")
conn.close()
