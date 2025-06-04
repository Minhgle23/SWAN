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
                "-jc",              # JS crawl
                       # robots.txt + sitemap.xml
                "-fx",              # form detection
                "-td",              # tech detect
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

        # Phân loại URL
        forms, apis, statics, others = self.classify_urls(all_links)

        data.urls.extend(sorted(all_links))
        data.form_links.extend(forms)
        data.api_links.extend(apis)
        data.static_links.extend(statics)

        print(f"\n[✓] Katana thu được: {len(all_links)} URL")
        print(f"   ├─ 🧪 Form URL    : {len(forms)}")
        print(f"   ├─ 🔌 API Endpoint: {len(apis)}")
        print(f"   └─ 📦 Static File : {len(statics)}")

        return data

    def name(self):
        return "Katana"

    def classify_urls(self, urls):
        forms, apis, statics, others = [], [], [], []

        for url in urls:
            u = url.lower()

            if any(x in u for x in [
            "/login", "/signin", "/signup", "/register", "/auth", "/form", "/contact",
            "?q=", "?search=", "?s="
            ]):
                forms.append(url)
            elif any(x in u for x in [
                "/api/", ".php", ".asp", ".aspx", ".jsp", ".do", ".cgi", ".json", ".action",
                "?id=", "?user=", "?page=", "?uid=", "?token="
            ]):
                apis.append(url)
            elif any(x in u for x in [
                ".js", ".ts", ".css", ".vue", ".jsx", ".png", ".jpg", ".jpeg", ".gif", ".svg", 
                ".woff", ".ttf", ".ico", ".eot", ".map"
            ]):
                statics.append(url)
            else:
                others.append(url)

        return forms, apis, statics, others


# # ✅ Test riêng
# if __name__ == "__main__":
#     from tool_data import ToolData
#     test_data = ToolData(alive_urls=["https://hackerone.com"])
#     result = KatanaTool().run(test_data)

#     print("\n🧪 FORM URL:")
#     for u in result.form_links:
#         print(" -", u)

#     print("\n🔌 API URL:")
#     for u in result.api_links:
#         print(" -", u)

#     print("\n📦 STATIC URL:")
#     for u in result.static_links:
#         print(" -", u)
