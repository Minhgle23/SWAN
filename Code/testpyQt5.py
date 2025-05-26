import sys
import subprocess
import threading
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit

class ScanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("URL Scan Tool")
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()
        self.label = QLabel("Nhập domain (ví dụ: example.com):")
        self.input = QLineEdit()
        self.btn_run = QPushButton("Bắt đầu quét")
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.output)
        self.setLayout(layout)

        self.btn_run.clicked.connect(self.start_scan)

    def start_scan(self):
        domain = self.input.text().strip()
        if not domain:
            self.output.setText("⚠️ Vui lòng nhập domain.")
            return
        self.output.setText(f"🔍 Đang quét: {domain}...\n")
        thread = threading.Thread(target=self.full_scan, args=(domain,))
        thread.start()

    def log(self, text):
        self.output.append(text)
        QApplication.processEvents()

    def run_script(self, script_name):
        self.log(f"▶️ Đang chạy: {script_name}...")
        try:
            result = subprocess.run(["python", script_name], capture_output=True, text=True, check=True)
            self.log(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Lỗi khi chạy {script_name}:\n{e.stderr.strip()}")

    def full_scan(self, domain):
        env = os.environ.copy()
        env["DOMAIN"] = domain  # nếu bạn muốn truyền biến môi trường

        # Ghi input cho subdomain.py
        with open("input_domain.txt", "w") as f:
            f.write(domain)

        # Chạy từng bước
        self.run_script("subdomain.py")
        self.run_script("resolve_IP.py")
        self.run_script("Web_recon.py")
        self.run_script("api_hunter_updated.py")

        self.log("\n✅ Quét hoàn tất. Kết quả được lưu trong thư mục D:/results")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ScanApp()
    win.show()
    sys.exit(app.exec_())
