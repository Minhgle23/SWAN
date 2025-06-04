import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class DalfoxTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running DalfoxTool...")

        output_file = Path("D:/results/xss_suspect.txt")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        xss_found = []

        if not data.xss_targets:
            print("⚠️ Không có URL nghi XSS.")
            return data

        for url in data.xss_targets:
            print(f"[→] Dalfox kiểm tra: {url}")
            cmd = ["D:/tools/dalfox.exe", "url", url, "--silence"]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                output = result.stdout.lower()

                if "vuln" in output or "[xss]" in output:
                    print(" [+] Nghi ngờ có XSS:", url)
                    xss_found.append(url)

            except subprocess.TimeoutExpired:
                print(" [-] Quá thời gian:", url)
            except Exception as e:
                print(" [-] Lỗi dalfox:", e)

        if xss_found:
            with output_file.open("w", encoding="utf-8") as f:
                f.write("\n".join(xss_found))
            print(f"[✓] Ghi {len(xss_found)} dòng nghi ngờ XSS vào {output_file}")

        data.xss_results = xss_found
        return data

    def name(self):
        return "Dalfox"
