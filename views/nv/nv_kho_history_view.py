# views/nv/nv_kho_history_view.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox
from PyQt6.QtCore import Qt

class NvKhoHistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = None # Sẽ được gán từ MainView
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.lbl_title = QLabel("📜 LỊCH SỬ NHẬP KHO CHI TIẾT")
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2e7d32;")
        layout.addWidget(self.lbl_title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7) 
        self.table.setHorizontalHeaderLabels([
            "Mã Phiếu", "Ngày Nhập", "Nhà Cung Cấp", 
            "Tên Sản Phẩm", "ĐVT", "Tổng Tiền", "Người Nhập"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch) # Tên SP rộng nhất
        self.table.setColumnWidth(4, 70) 
        
        self.table.verticalHeader().setDefaultSectionSize(50) 
        layout.addWidget(self.table)

    def display_data(self): 
        if not self.controller: 
            print("Chưa có controller")
            return
        try:
            data = self.controller.get_import_history()
            self.table.setRowCount(0)
            
            for row, item in enumerate(data):
                self.table.insertRow(row)
                
                # Cột 0, 1, 2: Mã, Ngày, NCC
                self.table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(str(item['ngay_nhap'])))
                self.table.setItem(row, 2, QTableWidgetItem(item['ten_ncc']))
                
                # Cột 3: Tên sản phẩm (Đã tách riêng trong SQL)
                item_ten = QTableWidgetItem(item.get('ds_ten_sp', ''))
                self.table.setItem(row, 3, item_ten)
                
                # Cột 4: ĐVT (Đã tách riêng trong SQL)
                item_dvt = QTableWidgetItem(item.get('ds_dvt', ''))
                item_dvt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 4, item_dvt)
                
                # Cột 5: Tổng tiền
                tien = float(item['tong_tien_nhap'] or 0)
                self.table.setItem(row, 5, QTableWidgetItem(f"{tien:,.0f} đ"))
                
                # Cột 6: Người nhập
                self.table.setItem(row, 6, QTableWidgetItem(item['ten_nv']))
                
            # Tự động chỉnh độ cao hàng để hiện hết các dòng sản phẩm bên trong
            self.table.resizeRowsToContents()
            
        except Exception as e:
            print(f"Lỗi khi đổ dữ liệu vào bảng: {e}")