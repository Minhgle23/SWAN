from tools.massdns_tool import MassdnsTool
from tool_data import ToolData
from tools.subfinder_tool import SubfinderTool
from tools.amass_tool import AmassTool
from tools.dnsx_tool import DnsxTool

def run_pipeline(domain: str):
    data = ToolData(domain=domain)

    tools = [
        SubfinderTool(),
        AmassTool(),
        DnsxTool(),
        MassdnsTool(),
    ]

    for tool in tools:
        print(f"\n▶ Running {tool.name()}...")
        data = tool.run(data)

    # loại bỏ trùng
    data.urls = sorted(set(data.urls))

    return data

def save_to_file(lines, filepath: str):
    from pathlib import Path
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"[✓] Đã lưu {len(lines)} dòng vào {filepath}")

if __name__ == "__main__":
    domain = input("Nhập domain: ").strip()
    result = run_pipeline(domain)

    save_to_file(result.urls, "D:/results/all_subs.txt")
    save_to_file(result.alive_urls or [domain], "D:/results/alive_subs.txt")

    print("\n========== KẾT QUẢ ==========")
    if result.alive_urls:
        for sub in result.alive_urls:
            print(sub)
        print(f"\nTổng cộng: {len(result.alive_urls)} / {len(result.urls)} subdomain đang hoạt động.")
    else:
        print("Không có subdomain hoạt động. Ghi domain:", domain)
