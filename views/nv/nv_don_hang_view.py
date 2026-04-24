from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QPushButton, QLabel, QComboBox, QHeaderView)
from PyQt6.QtCore import Qt

class NvDonHangView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # --- Thống kê ---
        stats_layout = QHBoxLayout()
        self.lbl_stats = QLabel("📊 Tổng số đơn: 0")
        self.lbl_stats.setStyleSheet("font-size: 16px; font-weight: bold; color: #1b5e20; padding: 10px;")
        
        self.btn_add = QPushButton("➕ Tạo đơn mới")
        self.btn_add.setStyleSheet("background-color: #2e7d32; color: white; padding: 8px 15px;")
        
        stats_layout.addWidget(self.lbl_stats)
        stats_layout.addStretch()
        stats_layout.addWidget(self.btn_add)
        layout.addLayout(stats_layout)

        # --- Bộ lọc ---
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Trạng thái:"))
        self.cb_status = QComboBox()
        self.cb_status.addItems(["Tất cả", "Chờ xác nhận", "Đang giao", "Đã giao", "Đã hủy"])
        filter_layout.addWidget(self.cb_status)
        filter_layout.addStretch()
        
        self.btn_refresh = QPushButton("🔄 Làm mới")
        filter_layout.addWidget(self.btn_refresh)
        layout.addLayout(filter_layout)

        # --- Bảng ---
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Ngày lập", "Khách hàng", "Địa chỉ", "Tổng tiền", "Trạng thái", "Thao tác"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)