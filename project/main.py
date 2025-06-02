from tool_data import ToolData
from tools.amass_tool import AmassTool 
from tools.subfinder_tool import SubfinderTool
from tools.dnsx_tool import DnsxTool
from tools.massdns_tool import MassdnsTool

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

    # 5. Massdns (dùng luôn biến alive)
    massdns_tool = MassdnsTool()
    resolver_input = ToolData(domain=domain, alive_urls=alive)
    result_massdns = massdns_tool.run(resolver_input)
    save_to_file(result_dir / "resolve_ips.txt", result_massdns.resolved_ips)


if __name__ == "__main__":
    main()