import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class HttpxTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running HttpxTool...")

        if not data.alive_urls:
            print("⚠️ Không có subdomain để kiểm tra HTTP.")
            return data

        # Ghi alive_urls ra file tạm
        input_path = Path("D:/results/httpx_input.txt")
        input_path.parent.mkdir(parents=True, exist_ok=True)
        with input_path.open("w", encoding="utf-8") as f:
            f.write("\n".join(data.alive_urls))

        cmd = [
            "D:/tools/httpx.exe",
            "-l", str(input_path),
            "-silent",
            "-status-code",
            "-title",
            "-tech-detect",
            "-web-server",
            "-ip",
            "-location",
            "-cdn",
            "-follow-redirects",
            "-timeout", "10",
            "-no-color"
        ]

        try:           
            result = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")

            if result.returncode != 0:
                print("❌ Httpx lỗi:", result.stderr)
                return data

            lines = result.stdout.strip().splitlines()
            data.httpx_results.extend(lines)

            print(f"[✓] httpx trả về {len(lines)} dòng.")
            for line in lines:
                print(" [+]", line)

        except Exception as e:
            print("❌ Lỗi khi chạy httpx:", e)

        return data

    def name(self):
        return "Httpx"

# ✅ Test riêng
# if __name__ == "__main__":
#     from tool_data import ToolData
#     test_data = ToolData(alive_urls=["google.com", "microsoft.com"])
#     result = HttpxTool().run(test_data)

#     print("\n🎯 Kết quả httpx:")
#     for r in result.httpx_results:
#         print(" -", r)
