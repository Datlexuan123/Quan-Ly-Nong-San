from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView, QLabel

class AdminDuyetHuyView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.lbl = QLabel("🔔 PHÊ DUYỆT BÁO HỦY HÀNG HÓA")
        self.lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #d32f2f;")
        layout.addWidget(self.lbl)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["NV báo", "Sản phẩm", "SL hủy", "Lý do", "Ngày", "Thao tác"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)