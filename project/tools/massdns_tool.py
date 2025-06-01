import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData
from pathlib import Path
import re

class MassdnsTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Đang chuẩn hóa subdomain và chạy massdns...")

        # === Ghi input vào file D:/results/alive_subs.txt ===
        alive_path = Path("D:/results/alive_subs.txt")
        alive_path.parent.mkdir(parents=True, exist_ok=True)

        # Làm sạch và chuẩn hóa subdomain
        cleaned = self._clean_domains(data.alive_urls)
        with alive_path.open("w", encoding="utf-8") as f:
            for d in cleaned:
                f.write(d + "\n")

        # === Gọi massdns trong WSL ===
        resolvers_path = Path("D:/wordlists/resolvers.txt")
        output_path = Path("D:/results/resolved_ip.txt")

        for path in [resolvers_path, alive_path]:
            if not path.exists():
                raise FileNotFoundError(f"❌ Không tìm thấy file: {path}")

        cmd = [
            "wsl",
            "~/massdns/bin/massdns",
            "-r", f"/mnt/d{resolvers_path.as_posix()[2:]}",
            "-o", "S",
            "-w", f"/mnt/d{output_path.as_posix()[2:]}",
            f"/mnt/d{alive_path.as_posix()[2:]}"
        ]

        print("➡️ Chạy massdns:")
        print(" ".join(cmd))

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ massdns lỗi:", result.stderr)
                return data

            # Trích xuất IP từ kết quả
            resolved_ips = self._parse_massdns_output(output_path)
            data.resolved_ips = resolved_ips
            print(f"✅ Đã resolve được {len(resolved_ips)} IP.")
            resolve_ip_path = Path("D:/results/Resolve_IP.txt")
            with resolve_ip_path.open("w", encoding="utf-8") as f:
                f.write("\n".join(resolved_ips))
            print(f"💾 Đã lưu IP vào {resolve_ip_path}")

        except Exception as e:
            print(f"❌ Lỗi khi chạy massdns: {e}")

        return data

    def name(self):
        return "Massdns"

    def _clean_domains(self, lines):
        cleaned = []
        for line in lines:
            line = line.strip()
            if line.startswith("http://") or line.startswith("https://"):
                line = line.replace("https://", "").replace("http://", "")
            domain = line.split("/")[0]
            if domain:
                cleaned.append(domain)
        return list(set(cleaned))

    def _parse_massdns_output(self, output_path: Path):
        resolved = []
        ip_regex = re.compile(r"A\s+(\d+\.\d+\.\d+\.\d+)")
        try:
            with output_path.open("r", encoding="utf-8") as f:
                for line in f:
                    match = ip_regex.search(line)
                    if match:
                        resolved.append(match.group(1))
        except Exception as e:
            print(f"❌ Lỗi đọc output massdns: {e}")
        return list(set(resolved))
