from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from config.database import get_connection

class AdminAddNCCView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Nhà Cung Cấp")
        self.setFixedSize(350, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel("NHÀ CUNG CẤP MỚI")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.txt_ten = QLineEdit(); self.txt_ten.setPlaceholderText("Tên nhà cung cấp")
        self.txt_sdt = QLineEdit(); self.txt_sdt.setPlaceholderText("Số điện thoại")
        self.txt_diachi = QLineEdit(); self.txt_diachi.setPlaceholderText("Địa chỉ")
        self.txt_ghichu = QLineEdit(); self.txt_ghichu.setPlaceholderText("Ghi chú")

        layout.addWidget(QLabel("Tên NCC:"))
        layout.addWidget(self.txt_ten)
        layout.addWidget(QLabel("Điện thoại:"))
        layout.addWidget(self.txt_sdt)
        layout.addWidget(QLabel("Địa chỉ:"))
        layout.addWidget(self.txt_diachi)
        layout.addWidget(QLabel("Ghi chú:"))
        layout.addWidget(self.txt_ghichu)

        self.btn_save = QPushButton("Lưu Nhà Cung Cấp")
        self.btn_save.setStyleSheet("background-color: #2e7d32; color: white; padding: 10px; font-weight: bold;")
        self.btn_save.clicked.connect(self.save_data)
        layout.addWidget(self.btn_save)

    def save_data(self):
        ten = self.txt_ten.text()
        sdt = self.txt_sdt.text()
        diachi = self.txt_diachi.text()
        ghichu = self.txt_ghichu.text()

        if not ten:
            QMessageBox.warning(self, "Lỗi", "Tên NCC không được để trống!")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Sửa lại cột INSERT cho khớp Database
            sql = "INSERT INTO nha_cung_cap (ten_ncc, so_dien_thoai, dia_chi, ghi_chu) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (ten, sdt, diachi, ghichu))
            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm: {e}")