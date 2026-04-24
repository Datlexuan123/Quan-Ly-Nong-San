from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt

class NvCaNhanView(QWidget):
    def __init__(self, user_info):
        super().__init__()
        # Đảm bảo user_info không bị None để tránh lỗi khi load giao diện
        self.user_info = user_info if user_info else {} 
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        
        # --- CỘT TRÁI: THÔNG TIN HỒ SƠ ---
        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ddd;")
        info_v = QVBoxLayout(info_frame)
        
        title_info = QLabel("👤 HỒ SƠ NHÂN VIÊN")
        title_info.setStyleSheet("font-size: 18px; font-weight: bold; color: #2E7D32; border: none; padding-bottom: 10px;")
        info_v.addWidget(title_info)
        
        # Lấy dữ liệu từ dict user_info (Sửa lại key cho khớp database)
        ho_ten = self.user_info.get('ho_ten', 'N/A')
        username = self.user_info.get('username', 'N/A') # Đã sửa từ ten_dang_nhap
        chuc_vu = self.user_info.get('chuc_vu', 'N/A')   # Đã sửa từ vai_tro
        
        info_v.addWidget(QLabel(f"<b>Họ và tên:</b> {ho_ten}"))
        info_v.addWidget(QLabel(f"<b>Tên đăng nhập:</b> {username}"))
        info_v.addWidget(QLabel(f"<b>Chức vụ:</b> {chuc_vu}"))
        info_v.addStretch()
        
        # --- CỘT PHẢI: ĐỔI MẬT KHẨU ---
        pwd_frame = QFrame()
        pwd_frame.setStyleSheet("background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd;")
        pwd_v = QVBoxLayout(pwd_frame)
        
        title_pwd = QLabel("🔑 ĐỔI MẬT KHẨU")
        title_pwd.setStyleSheet("font-size: 18px; font-weight: bold; color: #d32f2f; border: none; padding-bottom: 10px;")
        pwd_v.addWidget(title_pwd)
        
        pwd_v.addWidget(QLabel("Mật khẩu hiện tại:"))
        self.txt_old_pwd = QLineEdit()
        self.txt_old_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        pwd_v.addWidget(self.txt_old_pwd)
        
        pwd_v.addWidget(QLabel("Mật khẩu mới:"))
        self.txt_new_pwd = QLineEdit()
        self.txt_new_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        pwd_v.addWidget(self.txt_new_pwd)
        
        pwd_v.addWidget(QLabel("Xác nhận mật khẩu mới:"))
        self.txt_confirm_pwd = QLineEdit()
        self.txt_confirm_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        pwd_v.addWidget(self.txt_confirm_pwd)
        
        self.btn_update_pwd = QPushButton("Cập nhật mật khẩu")
        self.btn_update_pwd.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; padding: 10px; margin-top: 10px;")
        pwd_v.addWidget(self.btn_update_pwd)
        pwd_v.addStretch()

        layout.addWidget(info_frame, 1)
        layout.addWidget(pwd_frame, 1)