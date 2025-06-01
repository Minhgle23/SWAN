import json

# Đường dẫn tới file ffuf JSON
file_path = "D:/results/ffuf_test.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Lấy kết quả
results = data.get("results", [])

# In từng kết quả
for r in results:
    fuzz_value = r.get("input", {}).get("FUZZ", "")
    status = r.get("status")
    url = r.get("url", "N/A")
    print(f"[{status}] {url} (FUZZ='{fuzz_value}')")
