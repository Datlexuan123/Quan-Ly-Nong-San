# views/admin/admin_sanpham_view.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QLabel, QHeaderView, QLineEdit
from PyQt6.QtCore import Qt

class AdminSanPhamView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header: Tiêu đề và nút Thêm sản phẩm
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

        # Thanh tìm kiếm
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Tìm kiếm theo tên sản phẩm hoặc nguồn gốc...")
        self.txt_search.setFixedHeight(35)
        self.txt_search.setStyleSheet("border: 1px solid #ccc; border-radius: 15px; padding-left: 15px; margin-bottom: 10px;")
        layout.addWidget(self.txt_search)

        # Bảng dữ liệu: Đã tăng lên 8 cột để khớp với Controller
        self.table = QTableWidget()
        self.table.setColumnCount(9) 
        self.table.setHorizontalHeaderLabels([
          "Mã SP", "Hình ảnh", "Tên sản phẩm", "Giá vốn TB", "Giá bán", 
            "Số lượng tồn", "Hạn dùng", "Đơn vị tính", "Thao tác"
        ])
        
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(3, 100) # Độ rộng cho cột giá vốn
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) 
        
        layout.addWidget(self.table)