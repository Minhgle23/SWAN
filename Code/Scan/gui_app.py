import os
import sys
import subprocess
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# === Thread chạy quét ===
class RunnerThread(QThread):
    log_signal = pyqtSignal(str)
    def __init__(self, domain):
        super().__init__()
        self.domain = domain

    def run(self):
        scripts = [
            ["python", "subdomain.py", self.domain],
            ["python", "resolve_IP.py"],
            ["python", "Scan_Ports.py"],
            ["python", "Web_recon.py"],
            ["python", "api_hunter_updated.py"],
            ["python", "Database/save_subdomains.py"],
            ["python", "Database/save_dns_records.py"],
            ["python", "Database/save_portscan.py"],
            ["python", "Database/save_web_recon.py"],
        ]
        for cmd in scripts:
            self.log_signal.emit(f"\n▶ Đang chạy: {' '.join(cmd)}\n")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
                self.log_signal.emit(result.stdout)
                if result.stderr:
                    self.log_signal.emit(f"[Lỗi] {result.stderr}")
            except Exception as e:
                self.log_signal.emit(f"❌ Lỗi: {e}")

# === Giao diện chính ===
class ScanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛡️ Security Scan Tool")
        self.setGeometry(300, 200, 900, 600)

        # Layout
        self.layout = QVBoxLayout()

        self.label = QLabel("Nhập domain (vd: example.com):")
        self.domain_input = QLineEdit()

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        # ComboBox chọn database + bảng
        self.db_combo = QComboBox()
        self.db_combo.addItems([
            "dns_results.db:dns_records",
            "nmap_scan_results.db:port_scan_results",
            "web_recon.db:httpx_results"
        ])

        # Các nút
        btn_layout = QHBoxLayout()
        self.scan_button = QPushButton("🔍 Bắt đầu quét")
        self.view_button = QPushButton("📂 Xem dữ liệu")
        btn_layout.addWidget(self.scan_button)
        btn_layout.addWidget(self.view_button)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.domain_input)
        self.layout.addLayout(btn_layout)
        self.layout.addWidget(QLabel("🔽 Chọn database:bảng cần xem:"))
        self.layout.addWidget(self.db_combo)
        self.layout.addWidget(self.log_output)

        self.setLayout(self.layout)

        # Kết nối nút
        self.scan_button.clicked.connect(self.start_scan)
        self.view_button.clicked.connect(self.view_data)

    def start_scan(self):
        domain = self.domain_input.text().strip()
        if not domain:
            QMessageBox.warning(self, "Thiếu domain", "Vui lòng nhập domain để quét.")
            return
        self.scan_button.setEnabled(False)
        self.log_output.clear()
        self.thread = RunnerThread(domain)
        self.thread.log_signal.connect(self.append_log)
        self.thread.finished.connect(lambda: self.scan_button.setEnabled(True))
        self.thread.start()

    def view_data(self):
        try:
            selected = self.db_combo.currentText()
            db_name, table = selected.split(":")
            db_path = f"D:/results/{db_name}"

            if not os.path.exists(db_path):
                self.log_output.setPlainText(f"⚠️ Không tìm thấy: {db_path}")
                return

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()

            msg = f"📊 Dữ liệu từ {db_name} bảng {table} ({len(rows)} dòng):\n"
            msg += " | ".join(columns) + "\n"
            msg += "-" * 100 + "\n"
            for row in rows:
                msg += " | ".join(str(item) for item in row) + "\n"
            self.log_output.setPlainText(msg)

        except Exception as e:
            self.log_output.setPlainText(f"❌ Lỗi khi đọc DB: {e}")

    def append_log(self, message):
        self.log_output.append(message)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScanApp()
    window.show()
    sys.exit(app.exec_())
