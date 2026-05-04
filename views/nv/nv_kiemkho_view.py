from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QDoubleSpinBox, QTextEdit, QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt

class NvKiemKhoView(QWidget):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data if user_data else {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 30, 50, 30)

        # Khung tiêu đề
        self.lbl_title = QLabel("📦 KIỂM KHO & BÁO HỦY HÀNG HÓA")
        self.lbl_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1b5e20; margin-bottom: 20px;")
        layout.addWidget(self.lbl_title)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ddd;")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(15)

        # Chọn sản phẩm
        form_layout.addWidget(QLabel("<b>Chọn sản phẩm báo hủy:</b>"))
        self.cbo_sp = QComboBox()
        self.cbo_sp.setFixedHeight(40)
        form_layout.addWidget(self.cbo_sp)

        # Số lượng hủy
        form_layout.addWidget(QLabel("<b>Số lượng hủy:</b>"))
        self.spin_qty = QDoubleSpinBox()
        self.spin_qty.setRange(0.1, 1000.0)
        self.spin_qty.setFixedHeight(40)
        form_layout.addWidget(self.spin_qty)

        # Lý do hủy
        form_layout.addWidget(QLabel("<b>Lý do báo hủy:</b>"))
        self.txt_lydo = QTextEdit()
        self.txt_lydo.setPlaceholderText("Ví dụ: Hàng bị dập nát, hết hạn sử dụng...")
        self.txt_lydo.setFixedHeight(100)
        form_layout.addWidget(self.txt_lydo)

        # Nút xác nhận
        self.btn_confirm = QPushButton("XÁC NHẬN BÁO HỦY")
        self.btn_confirm.setFixedHeight(50)
        self.btn_confirm.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold; font-size: 16px; border: none; border-radius: 5px;")
        form_layout.addWidget(self.btn_confirm)

        layout.addWidget(form_frame)
        layout.addStretch()