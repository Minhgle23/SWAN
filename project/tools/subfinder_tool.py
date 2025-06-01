import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class SubfinderTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] SubfinderTool running...")
        try:
            result = subprocess.run(
                ["D:/tools/subfinder.exe", "-d", data.domain, "-silent"],
                capture_output=True, text=True, check=True
            )
            subdomains = result.stdout.strip().splitlines()
            data.urls.extend(subdomains)
        except subprocess.CalledProcessError as e:
            print("[-] Lỗi subfinder:", e)
        return data

    def name(self):
        return "Subfinder"
