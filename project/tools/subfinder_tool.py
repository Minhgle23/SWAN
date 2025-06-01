import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import subprocess
from tools.base_tool import BaseTool
from tool_data import ToolData

class KatanaTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running KatanaTool...")

        if not data.alive_urls:
            print("⚠️ Không có URL sống để crawl.")
            return data

        all_links = set()

        for url in data.alive_urls:
            cmd = [
                "D:/tools/katana.exe",
                "-u", url,
                "-silent",
                "-jc",             # crawl JS endpoint
                "-kf", "all",      # robots.txt + sitemap.xml
                "-fx",             # trích xuất form
                "-td",             # công nghệ sử dụng
                "-depth", "3"
            ]

            try:
                print(f"[→] Crawling: {url}")
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors="ignore")

                for line in process.stdout:
                    line = line.strip()
                    if line:
                        all_links.add(line)
                        print(" [+]", line)

                process.wait()
                if process.returncode != 0:
                    err = process.stderr.read()
                    print(f"[-] Katana lỗi với {url}:\n{err.strip()}")

            except Exception as e:
                print(f"❌ Lỗi khi chạy katana với {url}: {e}")

        data.urls.extend(sorted(all_links))
        print(f"[✓] Tổng cộng {len(all_links)} link thu được từ katana.")
        return data

    def name(self):
        return "Katana"

# ✅ Test riêng
if __name__ == "__main__":
    from tool_data import ToolData
    test_data = ToolData(alive_urls=["https://hackerone.com"])
    result = KatanaTool().run(test_data)

    print("\n🎯 Link thu được:")
    for link in result.urls:
        print(" -", link)
