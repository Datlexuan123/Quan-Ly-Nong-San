from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class OrderEditDialog(QDialog):
    def __init__(self, order_data):
        super().__init__()
        self.setWindowTitle(f"Sửa thông tin giao hàng - Đơn #{order_data['id']}")
        self.setFixedWidth(450)
        self.setStyleSheet("background-color: white; font-size: 14px;")
        
        layout = QVBoxLayout(self)

        # 1. Thông tin khách hàng (Chế độ chỉ đọc)
        layout.addWidget(QLabel("<b>👤 Khách hàng:</b>"))
        ten_kh = order_data.get('ten_khach') if order_data.get('ten_khach') else "Khách lẻ"
        self.txt_name = QLineEdit(ten_kh)
        self.txt_name.setReadOnly(True)
        self.txt_name.setStyleSheet("background-color: #f0f0f0; padding: 8px; border: 1px solid #ddd; border-radius: 4px;")
        layout.addWidget(self.txt_name)

        # 2. Thông tin địa chỉ (Cho phép nhân viên sửa)
        layout.addWidget(QLabel("<b>📍 Địa chỉ giao hàng:</b>"))
        self.txt_address = QTextEdit()
        # Lấy dữ liệu cũ từ bảng hoa_don
        dia_chi_cu = order_data.get('dia_chi_giao') if order_data.get('dia_chi_giao') else ""
        self.txt_address.setPlainText(dia_chi_cu)
        self.txt_address.setPlaceholderText("Nhập địa chỉ giao hàng mới...")
        self.txt_address.setStyleSheet("padding: 8px; border: 1px solid #4caf50; border-radius: 4px;")
        layout.addWidget(self.txt_address)

        # 3. Khu vực các nút bấm
        btn_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("Hủy bỏ")
        self.btn_cancel.setStyleSheet("padding: 10px; background-color: #f44336; color: white; border-radius: 4px; font-weight: bold;")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton("💾 Lưu cập nhật")
        self.btn_save.setStyleSheet("padding: 10px; background-color: #2e7d32; color: white; border-radius: 4px; font-weight: bold;")
        self.btn_save.clicked.connect(self.accept)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        
        layout.addLayout(btn_layout)

    def get_data(self):
        """Lấy địa chỉ mới từ Form để trả về cho Controller"""
        return self.txt_address.toPlainText().strip()