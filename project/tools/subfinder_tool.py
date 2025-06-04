import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class SubfinderTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running SubfinderTool...")

        if not data.domain:
            print("⚠️ Không có domain đầu vào.")
            return data

        try:
            result = subprocess.run(
                ["D:/tools/subfinder.exe", "-d", data.domain, "-silent"],
                capture_output=True, text=True, check=True
            )
            subdomains = result.stdout.strip().splitlines()
            data.urls.extend(subdomains)
            print(f"[✓] Subfinder tìm được {len(subdomains)} subdomain.")
        except subprocess.CalledProcessError as e:
            print("[-] Lỗi khi chạy subfinder:", e)

        return data

    def name(self):
        return "Subfinder"

# ✅ Tự chạy để test nếu gọi file này trực tiếp
# if __name__ == "__main__":
#     test_domain = "example.com"
#     tool = SubfinderTool()
#     result = tool.run(ToolData(domain=test_domain))

#     print("\n🎯 Kết quả:")
#     for sub in result.urls:
#         print(" -", sub)
