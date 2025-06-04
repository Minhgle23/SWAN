from pathlib import Path
from tool_data import ToolData
from tools.sqlmap_tool import SqlmapTool
from tools.dalfox_tool import DalfoxTool

def load_txt(path: str) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {path}")
        return []

def save_txt(path: str, lines: list[str]):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[✓] Đã ghi {len(lines)} dòng vào {path}")

def main():
    # Đọc dữ liệu đầu vào từ kết quả crawl
    api_links = load_txt("D:/results/katana_api_links.txt")
    all_links = load_txt("D:/results/katana_links.txt")

    # Lọc ra xss_targets (theo query đáng nghi)
    xss_targets = [url for url in all_links if any(p in url for p in ["?q=", "?search=", "?s="])]

    # Gán vào ToolData
    data = ToolData(api_links=api_links, xss_targets=xss_targets)

    # Chạy kiểm thử SQLi bằng sqlmap
    sqlmap_tool = SqlmapTool()
    data = sqlmap_tool.run(data)
    save_txt("D:/results/sql_suspect.txt", data.sqli_results)

    # Chạy kiểm thử XSS bằng dalfox
    dalfox_tool = DalfoxTool()
    data = dalfox_tool.run(data)
    save_txt("D:/results/xss_suspect.txt", data.xss_results)

    # Tổng kết
    print("\n🎯 Tổng kết A03:")
    print(f" - Số URL nghi SQLi: {len(data.sqli_results)}")
    print(f" - Số URL nghi XSS:  {len(data.xss_results)}")

    if not data.sqli_results and not data.xss_results:
        print("⚠️ Không phát hiện A03 → chuyển sang A05 (nếu muốn)")

if __name__ == "__main__":
    main()
