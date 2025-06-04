from pathlib import Path
from tool_data import ToolData
from tools.misconfig_tool import MisconfigTool
from tools.header_check_tool import HeaderCheckTool
from tools.nuclei_tool import NucleiTool

def load_alive_urls(path: str) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {path}")
        return []

def main():
    # Đường dẫn đầu vào (URL sống)
    alive_file = "D:/results/httpx_output.txt"

    # Load các URL còn sống
    alive_urls = load_alive_urls(alive_file)
    if not alive_urls:
        print("⚠️ Không có URL sống để kiểm thử A05.")
        return

    # Tạo đối tượng ToolData
    data = ToolData(alive_urls=alive_urls)

    # Chạy từng tool
    data = MisconfigTool().run(data)
    data = HeaderCheckTool().run(data)
    data = NucleiTool().run(data)

    # Hiển thị tổng kết
    print("\n🎯 Tổng kết A05:")
    print(f" - Endpoint nhạy cảm: {len(data.misconfig_results)}")
    print(f" - Thiếu header bảo mật: {len(data.header_issues)}")
    print(f" - Nuclei phát hiện: {len(data.nuclei_results)}")

    if data.misconfig_results:
        print("\n🔍 Một số file/endpoint nhạy cảm:")
        for x in data.misconfig_results[:5]:
            print("  -", x)
    if data.header_issues:
        print("\n🔍 Một số URL thiếu header:")
        for x in data.header_issues[:5]:
            print("  -", x)
    if data.nuclei_results:
        print("\n🔍 Một số kết quả từ nuclei:")
        for x in data.nuclei_results[:5]:
            print("  -", x)

if __name__ == "__main__":
    main()
