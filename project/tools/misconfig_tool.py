import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import requests
from tools.base_tool import BaseTool
from tool_data import ToolData

class MisconfigTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running MisconfigTool...")

        targets = data.alive_urls or []
        common_paths = [".env", ".git/config", "phpinfo.php", "backup.zip", "admin", "login", "db", "config.json"]
        found = []

        for base in targets:
            for path in common_paths:
                url = base.rstrip("/") + "/" + path
                try:
                    res = requests.get(url, timeout=5)
                    if res.status_code in [200, 403]:
                        print(f" [+] Found: {url} ({res.status_code})")
                        found.append(f"{url} [{res.status_code}]")
                except:
                    continue

        output_file = Path("D:/results/misconfig_found.txt")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text("\n".join(found), encoding="utf-8")
        data.misconfig_results = found
        return data

    def name(self):
        return "MisconfigTool"
