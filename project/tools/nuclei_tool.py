import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class NucleiTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running NucleiTool...")

        urls = data.alive_urls or []
        input_file = Path("D:/results/nuclei_input.txt")
        input_file.write_text("\n".join(urls), encoding="utf-8")

        output_file = Path("D:/results/nuclei_output.txt")
        cmd = [
            "nuclei",
            "-l", str(input_file),
            "-t", "misconfiguration",
            "-o", str(output_file),
            "-silent"
        ]

        try:
            subprocess.run(cmd, timeout=90)
        except Exception as e:
            print("[-] Lỗi chạy nuclei:", e)

        results = output_file.read_text(encoding="utf-8").splitlines() if output_file.exists() else []
        data.nuclei_results = results
        return data

    def name(self):
        return "NucleiTool"
