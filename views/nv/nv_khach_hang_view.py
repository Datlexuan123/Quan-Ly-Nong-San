from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QPushButton, QLineEdit, QLabel, QFrame, QHeaderView)
from PyQt6.QtCore import Qt

class NvKhachHangView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout()

        # --- BÊN TRÁI: DANH SÁCH ---
        left_container = QVBoxLayout()
        header = QLabel("QUẢN LÝ KHÁCH HÀNG")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2E7D32;")
        
        search_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Tìm tên hoặc SĐT...")
        self.btn_search = QPushButton("Tìm kiếm")
        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(self.btn_search)

        self.table = QTableWidget()
        # QUAN TRỌNG: Đã đổi thành 5 cột
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Họ Tên", "SĐT", "Địa Chỉ", "Điểm Tích Lũy"])
        
        # Cấu hình tự động giãn độ rộng các cột
        header_view = self.table.horizontalHeader()
        header_view.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Cột ID thu nhỏ
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Cột Điểm thu nhỏ
        
        left_container.addWidget(header)
        left_container.addLayout(search_layout)
        left_container.addWidget(self.table)

        # --- BÊN PHẢI: FORM ---
        self.detail_frame = QFrame()
        self.detail_frame.setFixedWidth(300)
        self.detail_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 10px;")
        form_layout = QVBoxLayout(self.detail_frame)

        form_layout.addWidget(QLabel("Họ tên:"))
        self.inp_ten = QLineEdit()
        form_layout.addWidget(self.inp_ten)

        form_layout.addWidget(QLabel("Số điện thoại:"))
        self.inp_sdt = QLineEdit()
        form_layout.addWidget(self.inp_sdt)

        form_layout.addWidget(QLabel("Địa chỉ:"))
        self.inp_dia_chi = QLineEdit()
        form_layout.addWidget(self.inp_dia_chi)

        self.btn_them = QPushButton("Thêm Khách")
        self.btn_them.setStyleSheet("background-color: #2E7D32; color: white; padding: 8px; font-weight: bold;")
        self.btn_lam_moi = QPushButton("Làm mới")
        
        form_layout.addWidget(self.btn_them)
        form_layout.addWidget(self.btn_lam_moi)
        form_layout.addStretch()

        self.main_layout.addLayout(left_container, 7)
        self.main_layout.addWidget(self.detail_frame, 3)
        self.setLayout(self.main_layout)