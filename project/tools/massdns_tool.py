import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
import re
from tools.base_tool import BaseTool
from tool_data import ToolData

class MassdnsTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running MassdnsTool...")

        if not data.alive_urls:
            print("⚠️ Không có subdomain sống để resolve.")
            return data

        # 1. Ghi danh sách alive subdomain vào file input
        input_path = Path("D:/results/alive_subs.txt")
        input_path.parent.mkdir(parents=True, exist_ok=True)
        with input_path.open("w", encoding="utf-8") as f:
            f.write("\n".join(data.alive_urls))

        # 2. Khai báo file resolver và output
        resolvers = Path("D:/wordlists/resolvers.txt")
        output_path = Path("D:/results/resolved_ip_raw.txt")

        if not resolvers.exists():
            print("❌ Không tìm thấy resolver list:", resolvers)
            return data

        # 3. Chạy massdns bằng WSL
        cmd = [
            "wsl",
            "~/massdns/bin/massdns",
            "-r", f"/mnt/d{resolvers.as_posix()[2:]}",
            "-o", "S",
            "-w", f"/mnt/d{output_path.as_posix()[2:]}",
            f"/mnt/d{input_path.as_posix()[2:]}"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Lỗi khi chạy massdns:", result.stderr)
                return data

            data.resolved_ips = self._parse_output(output_path)
            print(f"[✓] Đã resolve được {len(data.resolved_ips)} IP.")

        except Exception as e:
            print("❌ Exception khi chạy massdns:", e)

        return data

    def _parse_output(self, path: Path) -> list[str]:
        ip_regex = re.compile(r"A\s+(\d+\.\d+\.\d+\.\d+)")
        resolved = set()
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    match = ip_regex.search(line)
                    if match:
                        resolved.add(match.group(1))
        except Exception as e:
            print("❌ Lỗi khi đọc output massdns:", e)
        return sorted(resolved)

    def name(self):
        return "Massdns"

# ✅ Test trực tiếp
# if __name__ == "__main__":
#     from tool_data import ToolData
#     test_data = ToolData(alive_urls=["google.com", "microsoft.com"])
#     result = MassdnsTool().run(test_data)

    # print("\n🎯 Kết quả IP:")
    # for ip in result.resolved_ips:
    #     print(" -", ip)
