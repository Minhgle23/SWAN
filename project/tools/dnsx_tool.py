import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class DnsxTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] DnsxTool checking live subdomains...")
        try:
            result = subprocess.run(
                ["D:/tools/dnsx.exe", "-silent"],
                input="\n".join(data.urls),
                capture_output=True, text=True, check=True
            )
            alive = result.stdout.strip().splitlines()
            data.alive_urls = alive
        except subprocess.CalledProcessError as e:
            print("[-] Lỗi dnsx:", e)
        return data

    def name(self):
        return "Dnsx"
