import sys
import subprocess
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit
)
from PyQt5.QtCore import QThread, pyqtSignal

# === Cấu hình đường dẫn ===
SCAN_DIR = Path("D:/Code/Scan")
DB_DIR = Path("D:/Code/Database")
INPUT_FILE = SCAN_DIR / "input_domain.txt"

SCRIPTS = [
    SCAN_DIR / "subdomain.py",
    SCAN_DIR / "resolve_IP.py",
    SCAN_DIR / "Scan_Ports.py",
    SCAN_DIR / "Web_recon.py",
    SCAN_DIR / "api_hunter_updated.py",
    DB_DIR / "save_domain_status.py",
    DB_DIR / "Database_Resolve_IP.py",
    DB_DIR / "web_recon_DB.py"
]

# === Thread xử lý logic quét ===
class ScannerThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal()

    def __init__(self, domain):
        super().__init__()
        self.domain = domain

    def run(self):
        try:
            # Ghi domain vào input file
            with INPUT_FILE.open("w", encoding="utf-8") as f:
                f.write(self.domain)

            for script in SCRIPTS:
                if not script.exists():
                    self.log_signal.emit(f"❌ Không tìm thấy script: {script}")
                    continue

                self.log_signal.emit(f"\n▶️ Chạy script: {script.name}")
                try:
                    result = subprocess.run(
                        ["python", str(script)],
                        capture_output=True, text=True
                    )
                    if result.stdout.strip():
                        self.log_signal.emit(result.stdout.strip())
                    if result.stderr.strip():
                        self.log_signal.emit(f"[STDERR] {result.stderr.strip()}")
                except Exception as e:
                    self.log_signal.emit(f"❌ Lỗi khi chạy {script.name}: {e}")
        finally:
            self.done_signal.emit()


# === Giao diện chính ===
class ScanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Auto Security Scanner")
        self.setGeometry(100, 100, 800, 550)

        layout = QVBoxLayout()
        self.label = QLabel("🔎 Nhập domain (ví dụ: example.com):")
        self.input = QLineEdit()
        self.btn_run = QPushButton("🚀 Bắt đầu quét")
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

        self.output.clear()
        self.output.append(f"🔍 Bắt đầu quét domain: {domain}\n")

        self.btn_run.setEnabled(False)
        self.thread = ScannerThread(domain)
        self.thread.log_signal.connect(self.output.append)
        self.thread.done_signal.connect(self.scan_done)
        self.thread.start()

    def scan_done(self):
        self.output.append("\n✅ Quá trình quét hoàn tất. Kết quả lưu tại: D:/results")
        self.btn_run.setEnabled(True)

# === Chạy ứng dụng ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ScanApp()
    win.show()
    sys.exit(app.exec_())
