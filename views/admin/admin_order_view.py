from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLabel, QHeaderView
from PyQt6.QtCore import Qt

class AdminOrderView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.lbl_title = QLabel("QUẢN LÝ ĐƠN HÀNG")
        self.lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1b5e20; margin-bottom: 15px;")
        layout.addWidget(self.lbl_title)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Mã Đơn", "Ngày Lập", "Khách Hàng", "Tổng Tiền", "Trạng Thái", "Thanh Toán"
        ])
        
        # Làm bảng đẹp và bo góc giống trang Sản phẩm
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { border: none; background-color: white; border-radius: 10px; gridline-color: #f0f0f0; }
            QHeaderView::section { background-color: #f1f8e9; font-weight: bold; padding: 10px; border: none; }
        """)
        layout.addWidget(self.table)