import subprocess
import os

SCRIPTS = [
    "subdomain.py",
    "resolve_IP.py",
    "Scan_Ports.py",
    "Web_recon.py",
    "api_hunter_updated.py",
    "Database/save_subdomains.py",
    "Database/save_dns_records.py",
    "Database/save_portscan.py",
    "Database/save_web_recon.py",
    "Database/save_katana.py"
    "Database/save_ffuf_to_db.py"
]



def run_all():
    for script in SCRIPTS:
        print(f"\n▶ Running: {script}")
        try:
            subprocess.run(["python", script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Script lỗi: {script}\n{e}\n")

if __name__ == "__main__":
    os.chdir("D:/Code/Scan")
    run_all()
