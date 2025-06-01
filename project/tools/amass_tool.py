import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class AmassTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] AmassTool running...")
        try:
            result = subprocess.run(
                ["D:/tools/amass.exe", "enum", "-passive", "-d", data.domain],
                capture_output=True, text=True, check=True
            )
            subdomains = result.stdout.strip().splitlines()
            data.urls.extend(subdomains)
        except subprocess.CalledProcessError as e:
            print("[-] Lỗi amass:", e)
        return data

    def name(self):
        return "Amass"
