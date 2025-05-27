# main_app.py
import os
import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal


def safe_listdir(path):
    """Trả về danh sách file, thư mục trong path hoặc bỏ qua nếu không có quyền truy cập."""
    try:
        return os.listdir(path)
    except PermissionError:
        return []


def safe_walk(top):
    """
    Duyệt thư mục theo cách an toàn, bỏ qua thư mục bị giới hạn truy cập,
    ví dụ 'System Volume Information' trên Windows.
    """
    for root, dirs, files in os.walk(top):
        # Bỏ qua thư mục hệ thống 'System Volume Information' hoặc bất kỳ thư mục nào không muốn duyệt
        dirs[:] = [d for d in dirs if d != "System Volume Information"]

        # Thử lọc thư mục không truy cập được
        dirs_copy = dirs[:]
        for d in dirs_copy:
            full_path = os.path.join(root, d)
            try:
                os.listdir(full_path)
            except PermissionError:
                dirs.remove(d)  # Bỏ thư mục không truy cập được

        yield root, dirs, files


class RunnerThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, domain):
        super().__init__()
        self.domain = domain

    def run(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        scripts = [
            ["python", "subdomain.py", self.domain],
            ["python", "resolve_IP.py"],
            ["python", "Scan_Ports.py"],
            ["python", "Web_recon.py"],
            ["python", "api_hunter_updated.py"],
        ]

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
                result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
                self.log_signal.emit(result.stdout)

                if result.stderr:
                    # Nếu phát hiện lỗi EPERM trong stderr thì thông báo rõ ràng
                    if "EPERM" in result.stderr or "PermissionError" in result.stderr:
                        self.log_signal.emit("[Cảnh báo] Không có quyền truy cập một số thư mục (ví dụ: System Volume Information). Chương trình đã bỏ qua các thư mục này.\n")
                    else:
                        self.log_signal.emit(f"[Lỗi] {result.stderr}")
            except Exception as e:
                self.log_signal.emit(f"❌ Lỗi khi chạy {' '.join(cmd)}:\n{str(e)}\n")



class ScanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Security Scan Pipeline")
        self.setGeometry(300, 200, 700, 500)

        self.layout = QVBoxLayout()

        self.label = QLabel("Nhập domain (vd: example.com):")
        self.domain_input = QLineEdit()
        self.run_button = QPushButton("Bắt đầu quét")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.domain_input)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.log_output)

        self.setLayout(self.layout)

        self.run_button.clicked.connect(self.start_scan)

    def start_scan(self):
        domain = self.domain_input.text().strip()
        if not domain:
            QMessageBox.warning(self, "Thiếu domain", "Vui lòng nhập domain để quét.")
            return

        self.run_button.setEnabled(False)
        self.log_output.clear()
        self.thread = RunnerThread(domain)
        self.thread.log_signal.connect(self.append_log)
        self.thread.finished.connect(lambda: self.run_button.setEnabled(True))
        self.thread.start()

    def append_log(self, message):
        self.log_output.append(message)
        self.log_output.verticalScrollBar().setValue(self.log_output.verticalScrollBar().maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScanApp()
    window.show()
    sys.exit(app.exec_())
