from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QLabel, QHeaderView, QLineEdit
from PyQt6.QtCore import Qt

class AdminSanPhamView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        self.lbl_title = QLabel("QUẢN LÝ SẢN PHẨM")
        self.lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2e7d32;")
        
        self.btn_add = QPushButton("+ Sản phẩm")
        self.btn_add.setFixedSize(120, 40)
        self.btn_add.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold; border-radius: 5px;")
        
        header_layout.addWidget(self.lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_add)
        layout.addLayout(header_layout)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Tìm kiếm theo tên sản phẩm hoặc nguồn gốc...")
        self.txt_search.setFixedHeight(35)
        self.txt_search.setStyleSheet("border: 1px solid #ccc; border-radius: 15px; padding-left: 15px; margin-bottom: 10px;")
        layout.addWidget(self.txt_search)

        self.table = QTableWidget()
        # QUAN TRỌNG: Phải là 7 cột
        self.table.setColumnCount(7) 
        self.table.setHorizontalHeaderLabels([
            "Mã SP", "Tên sản phẩm", "Nguồn gốc", "Giá bán", "Số lượng tồn", "Hạn dùng", "Thao tác"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)