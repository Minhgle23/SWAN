import subprocess
import os

SCRIPTS = [
    "subdomain.py",
    "resolve_IP.py",
    "Scan_Ports.py",
    "Web_recon.py",
    "api_hunter_updated.py",
    "../Database/save_domain_status.py",
    "../Database/Database_Resolve_IP.py",
    "../Database/web_recon_DB.py"
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
