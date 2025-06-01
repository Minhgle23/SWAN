import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
import re
from tools.base_tool import BaseTool
from tool_data import ToolData

class NmapTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running NmapTool...")

        if not data.resolved_ips:
            print("⚠️ Không có IP để quét.")
            return data

        open_ports = set()

        for ip in data.resolved_ips:
            try:
                print(f"[→] Đang quét {ip} ...")
                result = subprocess.run(
                    ["nmap", "-Pn", "--top-ports", "100", ip],
                    capture_output=True, text=True, check=True
                )

                for line in result.stdout.splitlines():
                    match = re.match(r"^(\d+)/tcp\s+open", line)
                    if match:
                        port = int(match.group(1))
                        open_ports.add(port)

            except subprocess.CalledProcessError as e:
                print(f"[-] Lỗi khi quét {ip} bằng nmap: {e}")

        data.open_ports = sorted(open_ports)
        print(f"[✓] Tổng cộng {len(data.open_ports)} port mở.")
        return data

    def name(self):
        return "Nmap"

# ✅ Test trực tiếp
if __name__ == "__main__":
    from tool_data import ToolData
    data = ToolData(domain="test.com", resolved_ips=["8.8.8.8"])
    result = NmapTool().run(data)

    print("\n🎯 Các port mở:")
    for port in result.open_ports:
        print(" -", port)
