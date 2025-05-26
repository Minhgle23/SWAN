from config import ALIVE_SUBS, HTTPX, KATANA, FFUF, COMMON_WORDLIST
from pathlib import Path
import subprocess

# === KIỂM TRA FILE INPUT ===
if not ALIVE_SUBS.exists() or ALIVE_SUBS.stat().st_size == 0:
    print("⚠️ Không có domain hoạt động để quét Web.")
    exit()

# === CẤU HÌNH ===
output_base = Path("D:/results/web_recon")
httpx_out = output_base / "httpx_output.txt"
httpx_summary = output_base / "httpx_summary.txt"
katana_out = output_base / "katana"
ffuf_out = output_base / "ffuf"

# === TẠO THƯ MỤC ===
output_base.mkdir(parents=True, exist_ok=True)
katana_out.mkdir(parents=True, exist_ok=True)
ffuf_out.mkdir(parents=True, exist_ok=True)

# === 1. Đọc domain, thêm https:// ===
with ALIVE_SUBS.open("r") as f:
    urls = [f"https://{line.strip()}" for line in f if line.strip()]

Path("httpx_targets.txt").write_text("\n".join(urls), encoding="utf-8")

# === 2. Run httpx ===
print("[+] Running httpx...")
subprocess.run([
    str(HTTPX), "-l", "httpx_targets.txt", "-title", "-status-code",
    "-tech-detect", "-content-length", "-o", str(httpx_out)
])

# === 2.1 In và lưu kết quả httpx đẹp ===
def print_and_save_httpx_results(file_path, save_path):
    lines_out = []

    header = "\n📦 [1] HTTPX KẾT QUẢ:\n" + "-" * 80 + "\n"
    header += f"{'URL':<45} {'CODE':<6} {'SERVER':<12} {'TITLE'}\n"
    header += "-" * 80
    lines_out.append(header)

    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" ")
            url = parts[0]
            status = parts[1].strip("[]") if len(parts) > 1 else ""
            tech = parts[2].strip("[]") if len(parts) > 2 else ""
            content_type = parts[3].strip("[]") if len(parts) > 3 else ""
            title = " ".join(parts[4:]).replace("[title:", "").replace("]", "").strip(": ")

            formatted = f"{url:<45} {status:<6} {tech:<12} {title}"
            print(formatted)
            lines_out.append(formatted)

    lines_out.append("-" * 80)
    save_path.write_text("\n".join(lines_out), encoding="utf-8")
    print(f"\n[+] Đã lưu trình bày HTTPX vào: {save_path}")

print_and_save_httpx_results(httpx_out, httpx_summary)

# === 3. katana ===
print("[+] Running katana...")
for url in urls:
    domain = url.split("//")[1].replace(".", "_")
    out_file = katana_out / f"{domain}.txt"
    subprocess.run([str(KATANA), "-u", url, "-o", str(out_file)])

# === 4. ffuf ===
print("[+] Running ffuf...")
for url in urls:
    domain = url.split("//")[1].replace(".", "_")
    out_file = ffuf_out / f"{domain}.json"

    subprocess.run([
        str(FFUF), "-u", f"{url}/FUZZ", "-w", str(COMMON_WORDLIST),
        "-mc", "200,403", "-o", str(out_file), "-of", "json"
    ])
