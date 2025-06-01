import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class DnsxTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running DnsxTool...")

        if not data.urls:
            print("⚠️ Không có subdomain đầu vào để kiểm tra.")
            return data

        try:
            result = subprocess.run(
                ["D:/tools/dnsx.exe", "-silent"],
                input="\n".join(data.urls),
                capture_output=True, text=True, check=True
            )
            alive = result.stdout.strip().splitlines()
            data.alive_urls = alive
            print(f"[✓] Dnsx tìm được {len(alive)} subdomain sống.")
        except subprocess.CalledProcessError as e:
            print("[-] Lỗi khi chạy dnsx:", e)

        return data

    def name(self):
        return "Dnsx"

# ✅ Tự chạy để test nếu gọi trực tiếp
if __name__ == "__main__":
    test_subs = ["www.google.com", "notreal.abc.test"]
    from tool_data import ToolData

    data = ToolData(domain="test.com", urls=test_subs)
    result = DnsxTool().run(data)

    print("\n🎯 Subdomain sống:")
    for sub in result.alive_urls:
        print(" -", sub)
