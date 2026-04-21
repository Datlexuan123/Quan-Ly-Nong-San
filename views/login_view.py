from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt

# Sửa dòng này: Đảm bảo là LoginView (viết hoa)
class LoginView(QWidget): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng Nhập - Nông Sản Sạch")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #f0f4f0;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Khung chính
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: white; border-radius: 15px; border: 1px solid #ddd;")
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(30, 40, 30, 40)

        # Tiêu đề
        title = QLabel("HỆ THỐNG QUẢN LÝ")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #2e7d32; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Ô nhập liệu
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Tên đăng nhập")
        self.txt_username.setStyleSheet("padding: 12px; border: 1px solid #ddd; border-radius: 5px;")

        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("Mật khẩu")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setStyleSheet("padding: 12px; border: 1px solid #ddd; border-radius: 5px;")

        # Nút bấm
        self.btn_login = QPushButton("ĐĂNG NHẬP")
        self.btn_login.setStyleSheet("""
            QPushButton { background-color: #2e7d32; color: white; padding: 12px; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #388e3c; }
        """)

        frame_layout.addWidget(title)
        frame_layout.addSpacing(30)
        frame_layout.addWidget(self.txt_username)
        frame_layout.addWidget(self.txt_password)
        frame_layout.addSpacing(20)
        frame_layout.addWidget(self.btn_login)
        
        layout.addWidget(self.frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # QUAN TRỌNG: Thiết lập layout
        self.setLayout(layout)