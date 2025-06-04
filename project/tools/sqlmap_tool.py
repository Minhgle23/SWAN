import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
import json
import requests
from urllib.parse import urlparse, parse_qs
from tools.base_tool import BaseTool
from tool_data import ToolData

class SqlmapTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running SqlmapTool...")

        sqlmap_path = "D:/tools/sqlmapproject-sqlmap-f969dd8/sqlmap.py"
        output_file = Path("D:/results/sql_suspect.txt")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not data.api_links:
            print("⚠️ Không có API link để kiểm thử SQLi.")
            return data

        sqli_found = []

        for url in data.api_links:
            if "%5c" in url.lower() or "\\" in url:
                print(f"⚠️ Bỏ qua (encoding lỗi): {url}")
                continue

            if any(url.lower().endswith(ext) for ext in [".json", ".js", ".png", ".jpg", ".css"]):
                print(f"⚠️ Bỏ qua (static file): {url}")
                continue

            parsed = urlparse(url)
            params = parse_qs(parsed.query)

            if not params:
                print(f"⚠️ Bỏ qua (không có tham số): {url}")
                continue

            if not any(k.lower() in ["id", "uid", "user", "pid", "ref", "token"] for k in params.keys()):
                print(f"⚠️ Bỏ qua (tham số không nghi ngờ): {url}")
                continue

            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 404:
                    print(f"⚠️ Bỏ qua vì 404: {url}")
                    continue
            except:
                print(f"⚠️ Không truy cập được: {url}")
                continue

            print(f"[→] Kiểm tra SQLi: {url}")
            cmd = [
                "python", sqlmap_path,
                "-u", url,
                "--batch",
                "--level", "2",
                "--risk", "1",
                "--timeout", "10",
                "--technique", "B",
                "--flush-session",
                "--ignore-code", "404",
                "--answers=follow=Y"
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode != 0:
                    print(f"[-] sqlmap lỗi với {url}:")
                    print(result.stdout)
                    print(result.stderr)
                    continue

                output = result.stdout.lower()
                if "is vulnerable" in output or "parameter" in output:
                    print(" [+] Nghi ngờ có SQLi:", url)
                    sqli_found.append(url)

            except subprocess.TimeoutExpired:
                print(" [-] Quá thời gian:", url)
            except Exception as e:
                print(" [-] Lỗi sqlmap:", e)

        if sqli_found:
            with output_file.open("w", encoding="utf-8") as f:
                f.write("\n".join(sqli_found))
            print(f"[✓] Ghi {len(sqli_found)} dòng nghi ngờ SQLi vào {output_file}")
        else:
            output_file.write_text("")

        data.sqli_results = sqli_found
        return data

    def name(self):
        return "Sqlmap"

# if __name__ == "__main__":
#     file_path = Path("D:/results/katana_api_links.txt")
#     if file_path.exists():
#         with file_path.open("r", encoding="utf-8") as f:
#             api_links = [line.strip() for line in f if line.strip()]
#     else:
#         api_links = ["http://testphp.vulnweb.com/listproducts.php?cat=1"]

#     data = ToolData(api_links=api_links)
#     result = SqlmapTool().run(data)

#     print("\n🎯 URL nghi ngờ SQLi:")
#     for url in result.sqli_results:
#         print(" -", url)