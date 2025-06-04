import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import requests
from tools.base_tool import BaseTool
from tool_data import ToolData

class HeaderCheckTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running HeaderCheckTool...")

        required_headers = [
            "Content-Security-Policy", "X-Content-Type-Options",
            "Strict-Transport-Security", "X-Frame-Options", "Referrer-Policy"
        ]
        urls = data.alive_urls or []
        weak = []

        for url in urls:
            try:
                res = requests.get(url, timeout=5)
                missing = [h for h in required_headers if h not in res.headers]
                if missing:
                    print(f" [-] {url} thiếu: {', '.join(missing)}")
                    weak.append(f"{url} thiếu: {', '.join(missing)}")
            except:
                continue

        output_file = Path("D:/results/missing_headers.txt")
        output_file.write_text("\n".join(weak), encoding="utf-8")
        data.header_issues = weak
        return data

    def name(self):
        return "HeaderCheckTool"
