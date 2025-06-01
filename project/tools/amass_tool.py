import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class AmassTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running AmassTool...")

        if not data.domain:
            print("⚠️ Không có domain đầu vào.")
            return data

        try:
            result = subprocess.run(
                ["D:/tools/amass.exe", "enum", "-passive", "-d", data.domain],
                capture_output=True, text=True, check=True
            )
            subdomains = result.stdout.strip().splitlines()
            data.urls.extend(subdomains)
            print(f"[✓] Amass tìm được {len(subdomains)} subdomain.")
        except subprocess.CalledProcessError as e:
            print("[-] Lỗi khi chạy amass:", e)

        return data

    def name(self):
        return "Amass"

# ✅ Tự chạy để test nếu gọi file này trực tiếp
if __name__ == "__main__":
    test_domain = "example.com"
    tool = AmassTool()
    result = tool.run(ToolData(domain=test_domain))

    print("\n🎯 Kết quả:")
    for sub in result.urls:
        print(" -", sub)
