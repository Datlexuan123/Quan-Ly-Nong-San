from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QLabel, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from config.database import get_connection

class AdminAddNhanVienView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Nhân Viên Mới")
        self.setFixedSize(400, 450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("THÔNG TIN NHÂN VIÊN MỚI")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2e7d32;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.txt_ma = QLineEdit(); self.txt_ma.setPlaceholderText("Mã nhân viên (VD: NV006)")
        self.txt_ten = QLineEdit(); self.txt_ten.setPlaceholderText("Họ và tên")
        self.txt_user = QLineEdit(); self.txt_user.setPlaceholderText("Tên đăng nhập")
        self.txt_pass = QLineEdit(); self.txt_pass.setPlaceholderText("Mật khẩu")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.cbo_role = QComboBox()
        self.cbo_role.addItems(["nhanvien", "admin"])

        layout.addWidget(QLabel("Mã nhân viên:"))
        layout.addWidget(self.txt_ma)
        layout.addWidget(QLabel("Họ tên:"))
        layout.addWidget(self.txt_ten)
        layout.addWidget(QLabel("Tài khoản:"))
        layout.addWidget(self.txt_user)
        layout.addWidget(QLabel("Mật khẩu:"))
        layout.addWidget(self.txt_pass)
        layout.addWidget(QLabel("Chức vụ:"))
        layout.addWidget(self.cbo_role)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Lưu thông tin")
        self.btn_save.setStyleSheet("background-color: #2e7d32; color: white; padding: 10px; font-weight: bold;")
        self.btn_save.clicked.connect(self.save_employee)
        
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

    def save_employee(self):
        ma = self.txt_ma.text(); ten = self.txt_ten.text()
        user = self.txt_user.text(); pwd = self.txt_pass.text()
        role = self.cbo_role.currentText()

        if not all([ma, ten, user, pwd]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO nhan_vien (ma_nv, ho_ten, username, password, chuc_vu, trang_thai) VALUES (%s, %s, %s, %s, %s, 0)"
            cursor.execute(sql, (ma, ten, user, pwd, role))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Thành công", "Đã thêm nhân viên mới!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm nhân viên: {e}")