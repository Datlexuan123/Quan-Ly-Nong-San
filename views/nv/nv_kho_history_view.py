from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton

class NvKhoHistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Mã Phiếu", "Ngày Nhập", "Nhà Cung Cấp", "Tổng Tiền", "Người Nhập"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        
    def display_data(self, data):
        self.table.setRowCount(0)
        for row, item in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(item['ngay_nhap'])))
            self.table.setItem(row, 2, QTableWidgetItem(item['ten_ncc']))
            # Khớp với key tong_tien_nhap từ Model
            self.table.setItem(row, 3, QTableWidgetItem(f"{item['tong_tien_nhap']:,} đ"))
            self.table.setItem(row, 4, QTableWidgetItem(item['ten_nv']))