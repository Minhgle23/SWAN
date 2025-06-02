from tool_data import ToolData
from tools.subfinder_tool import SubfinderTool
from tools.amass_tool import AmassTool
from tools.dnsx_tool import DnsxTool
from tools.httpx_tool import HttpxTool
from tools.katana_tool import KatanaTool
from tools.ffuf_tool import FfufTool
from tools.massdns_tool import MassdnsTool
from tools.nmap import NmapTool

from concurrent.futures import ThreadPoolExecutor


def run_pipeline(domain: str):
    print(f"\n🚀 Bắt đầu quét với domain: {domain}")
    data = ToolData(domain=domain)

    # 1. Subdomain discovery (subfinder + amass)
    print("\n🔍 Thu thập subdomain...")
    for tool in [SubfinderTool(), AmassTool()]:
        data = tool.run(data)
    data.urls = sorted(set(data.urls))

    # 2. Alive check (dnsx)
    print("\n🌐 Kiểm tra subdomain sống...")
    data = DnsxTool().run(data)

    # 3. Httpx + Katana song song
    print("\n🌐 HTTP info + Web crawler (song song)...")
    with ThreadPoolExecutor() as executor:
        fut_httpx = executor.submit(HttpxTool().run, data)
        fut_katana = executor.submit(KatanaTool().run, data)
        data = fut_httpx.result()
        data = fut_katana.result()

    # 4. Fuzz endpoint (ffuf)
    print("\n💥 Fuzz endpoint với ffuf...")
    data = FfufTool().run(data)

    # 5. Resolve IP (massdns)
    print("\n🌍 Resolve IP với massdns...")
    data = MassdnsTool().run(data)

    # 6. Port scan (nmap)
    print("\n🔓 Quét port với Nmap...")
    data = NmapTool().run(data)

    # Tổng kết
    print("\n🎯 TỔNG KẾT:")
    print(f" - Tổng subdomain     : {len(data.urls)}")
    print(f" - Subdomain sống     : {len(data.alive_urls)}")
    print(f" - Katana thu được    : {len(data.urls)} link")
    print(f"   ├─ Form link        : {len(data.form_links)}")
    print(f"   ├─ API link         : {len(data.api_links)}")
    print(f" - FFUF kết quả       : {len(data.ffuf_paths)}")
    print(f" - IP resolved        : {len(data.resolved_ips)}")
    print(f" - Port mở (Nmap)     : {len(data.open_ports)}")

    return data


if __name__ == "__main__":
    domain = input("🌐 Nhập domain (ví dụ: example.com): ").strip()
    if domain:
        run_pipeline(domain)
    else:
        print("⚠️ Vui lòng nhập domain hợp lệ.")
