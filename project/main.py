from tool_data import ToolData
from tools.amass_tool import AmassTool 
from tools.subfinder_tool import SubfinderTool
from tools.dnsx_tool import DnsxTool
from tools.massdns_tool import MassdnsTool
from tools.nmap import NmapTool
from tools.katana_tool import KatanaTool
from tools.httpx_tool import HttpxTool
from tools.ffuf_tool import FfufTool
from tools.sqlmap_tool import SqlmapTool
from tools.sqlmap_tool import SqlmapTool
from tools.dalfox_tool import DalfoxTool
from urllib.parse import urlparse
from pathlib import Path

def clean_domain(raw: str) -> str:
    parsed = urlparse(raw)
    return parsed.netloc.strip("/") if parsed.scheme else raw.strip("/")

def save_to_file(path: str, lines: list[str]):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"[✓] Đã ghi {len(lines)} dòng vào {path}")
    except Exception as e:
        print(f"❌ Không thể ghi file {path}: {e}")

def load_from_file(path: str) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {path}")
        return []

def main():
    raw_input_domain = input("🔍 Nhập domain để kiểm tra: ").strip()
    domain = clean_domain(raw_input_domain)

    if not domain:
        print("❌ Domain không hợp lệ.")
        return

    result_dir = Path("D:/results")
    result_dir.mkdir(parents=True, exist_ok=True)

    # 1. Amass
    amass_tool = AmassTool()
    data_amass = amass_tool.run(ToolData(domain=domain))
    save_to_file(result_dir / "amass.txt", data_amass.urls)

    # 2. Subfinder
    subfinder_tool = SubfinderTool()
    data_sub = subfinder_tool.run(ToolData(domain=domain))
    save_to_file(result_dir / "subfinder.txt", data_sub.urls)

    # 3. Gộp và loại trùng
    combined = sorted(set(data_amass.urls + data_sub.urls))
    save_to_file(result_dir / "all_subdomain.txt", combined)

    # 4. Dnsx
    dnsx_tool = DnsxTool()
    data_input = ToolData(domain=domain, urls=combined)
    result_dnsx = dnsx_tool.run(data_input)

    alive = result_dnsx.alive_urls
    alive_path = result_dir / "alive_subs.txt"
    if alive:
        save_to_file(alive_path, alive)
    else:
        alive = [domain]
        save_to_file(alive_path, alive)
        print("⚠️ Không có subdomain sống, đã ghi lại domain gốc.")

    # 5. Massdns
    massdns_tool = MassdnsTool()
    resolver_input = ToolData(domain=domain, alive_urls=alive)
    result_massdns = massdns_tool.run(resolver_input)
    resolved_ip_path = result_dir / "resolve_ips.txt"
    save_to_file(resolved_ip_path, result_massdns.resolved_ips)

    # 6. Nmap scan từ resolve_ips.txt
    resolved_ips = load_from_file(str(resolved_ip_path))
    if resolved_ips:
        nmap_tool = NmapTool()
        data_nmap = ToolData(resolved_ips=resolved_ips)
        result_nmap = nmap_tool.run(data_nmap)
        save_to_file(result_dir / "nmap_ports.txt", [str(p) for p in result_nmap.open_ports])
    else:
        print("⚠️ Không có IP nào để chạy Nmap.")

    # 7. Katana - Crawl nội dung từ alive_subs
    katana_tool = KatanaTool()
    data_katana = katana_tool.run(ToolData(domain=domain, alive_urls=alive))
    save_to_file(result_dir / "katana_links.txt", data_katana.urls)
    save_to_file(result_dir / "katana_form_links.txt", data_katana.form_links)
    save_to_file(result_dir / "katana_api_links.txt", data_katana.api_links)
    save_to_file(result_dir / "katana_static_links.txt", data_katana.static_links)

    # 8. Httpx - Quét HTTP title/status/tech từ alive_subs
    httpx_tool = HttpxTool()
    data_httpx = httpx_tool.run(ToolData(domain=domain, alive_urls=alive))
    save_to_file(result_dir / "httpx_output.txt", data_httpx.httpx_results)

    # 9. Ffuf - Fuzz các form/api link từ Katana
    ffuf_tool = FfufTool()
    data_ffuf = ffuf_tool.run(ToolData(
        domain=domain,
        api_links=data_katana.api_links,
        form_links=data_katana.form_links
    ))
    save_to_file(result_dir / "ffuf_paths.txt", data_ffuf.ffuf_paths)

   
    # 10. Kiểm thử SQL Injection
    sqlmap_tool = SqlmapTool()
    data_sqlmap = sqlmap_tool.run(ToolData(api_links=data_katana.api_links))
    save_to_file(result_dir / "sql_suspect.txt", data_sqlmap.sqli_results)

    # 11. Chuẩn bị tập XSS target
    xss_candidates = [url for url in data_katana.urls if any(p in url for p in ["?q=", "?search=", "?s="])]
    xss_tool = DalfoxTool()
    data_xss = xss_tool.run(ToolData(xss_targets=xss_candidates))
    save_to_file(result_dir / "xss_suspect.txt", data_xss.xss_results)

    # 12. Kiểm tra có log hay không
    if not data_sqlmap.sqli_results and not data_xss.xss_results:
        print("⚠️ Không phát hiện A03 (SQLi/XSS) → Tiếp tục sang A05")
    else:
        if data_sqlmap.sqli_results:
            print("🛡️ [A03: SQLi] Phát hiện:", len(data_sqlmap.sqli_results))
        if data_xss.xss_results:
            print("🛡️ [A03: XSS] Phát hiện:", len(data_xss.xss_results))



if __name__ == "__main__":
    main()
