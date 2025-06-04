import sys
from pathlib import Path
import subprocess
import json
from tools.base_tool import BaseTool
from tool_data import ToolData

class FfufTool(BaseTool):
    def run(self, data: ToolData) -> ToolData:
        print("[*] Running FfufTool...")

        wordlist = Path("D:/wordlists/common.txt")
        if not wordlist.exists():
            print("❌ Không tìm thấy wordlist:", wordlist)
            return data

        all_results = set()

        # Ưu tiên fuzz trên API và FORM URL (nếu có)
        fuzz_targets = data.api_links + data.form_links
        if not fuzz_targets:
            print("⚠️ Không có URL từ api_links hoặc form_links để fuzz.")
            return data

        for url in fuzz_targets:
            # Chuyển URL thành dạng chuẩn nếu thiếu http
            if not url.startswith("http"):
                url = "http://" + url

            # Tạo tên file lưu output
            safe_name = url.replace("://", "_").replace("/", "_").replace("?", "_")
            output_dir = Path("D:/results/ffuf")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{safe_name}.json"


            # Chọn chế độ fuzz: path hay param
            if "/FUZZ" in url or url.endswith("/"):
                target_url = f"{url.rstrip('/')}/FUZZ"
            else:
                target_url = f"{url}?FUZZ=test"

            cmd = [
                "ffuf",
                "-u", target_url,
                "-w", str(wordlist),
                "-mc", "200,403,401",
                "-t", "50",
                "-of", "json",
                "-o", str(output_file)
            ]

            try:
                print(f"[→] Fuzzing: {target_url}")
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode != 0:
                    print(f"[-] ffuf lỗi với {url}:\n{result.stderr}")
                    continue

                # Đọc kết quả JSON
                if output_file.exists():
                    with output_file.open("r", encoding="utf-8") as f:
                        data_json = json.load(f)
                        for r in data_json.get("results", []):
                            fuzz_value = r.get("input", {}).get("FUZZ")
                            if fuzz_value:
                                full = target_url.replace("FUZZ", fuzz_value)
                                all_results.add(full)

            except Exception as e:
                print(f"❌ Lỗi khi chạy ffuf với {url}: {e}")

        data.ffuf_paths = sorted(all_results)
        print(f"[✓] Ffuf tìm được {len(data.ffuf_paths)} đường dẫn/phản hồi.")
        return data

    def name(self):
        return "Ffuf"

# ✅ Test riêng
# if __name__ == "__main__":
#     from tool_data import ToolData
#     test = ToolData(
#         api_links=["http://testphp.vulnweb.com/artists.php"],
#         form_links=["http://testphp.vulnweb.com/login.php"]
#     )
#     result = FfufTool().run(test)

#     print("\n🎯 Kết quả Ffuf:")
#     for path in result.ffuf_paths:
#         print(" -", path)
