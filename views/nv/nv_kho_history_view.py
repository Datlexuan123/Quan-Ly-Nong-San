from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from controllers.nv_nhaphang_controller import NvNhapHangController

class NvKhoHistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = NvNhapHangController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.lbl_title = QLabel("📜 LỊCH SỬ NHẬP KHO (Nhấn đúp để xem chi tiết sản phẩm)")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2e7d32;")
        layout.addWidget(self.lbl_title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Mã Phiếu", "Ngày Nhập", "Nhà Cung Cấp", "Tổng Tiền", "Tổng SL", "Người Nhập"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Kết nối sự kiện nhấn đúp chuột vào dòng
        self.table.cellDoubleClicked.connect(self.show_details)
        
        layout.addWidget(self.table)
        self.load_data()

    def load_data(self):
        data = self.controller.get_import_history()
        self.table.setRowCount(0)
        for row, item in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(item['ngay_nhap'])))
            self.table.setItem(row, 2, QTableWidgetItem(item['ten_ncc']))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item['tong_tien_nhap']:,.0f} đ"))
            self.table.setItem(row, 4, QTableWidgetItem(str(int(item['tong_sl_nhap']))))
            self.table.setItem(row, 5, QTableWidgetItem(item['ten_nv']))

    def show_details(self, row, column):
        """Hàm hiện chi tiết tên sản phẩm, SL và Giá khi nhấn vào mã phiếu"""
        # Lấy mã phiếu từ cột đầu tiên của dòng vừa nhấn
        ma_phieu = self.table.item(row, 0).text()
        
        # Gọi hàm lấy chi tiết từ model
        from models.nhaphang_model import NhapHangModel
        model = NhapHangModel()
        details = model.get_import_details(ma_phieu)
        
        if not details:
            QMessageBox.information(self, "Thông tin", f"Không tìm thấy dữ liệu chi tiết cho phiếu #{ma_phieu}.")
            return

        # Tạo chuỗi văn bản để hiển thị lên hộp thoại
        msg = f"--- CHI TIẾT PHIẾU NHẬP #{ma_phieu} ---\n\n"
        msg += f"{'Tên sản phẩm':<25} | {'SL':<5} | {'Giá nhập':<10}\n"
        msg += "-" * 50 + "\n"
        
        for d in details:
            ten = d.get('ten_sp', 'N/A')
            sl = d.get('so_luong_nhap', 0)
            gia = d.get('gia_nhap', 0)
            msg += f"• {ten:<23} | {sl:<5} | {gia:,.0f}đ\n"
        
        # Hiển thị kết quả ra màn hình
        QMessageBox.information(self, f"Chi tiết sản phẩm nhập", msg)

    def display_data(self, data):
        """Hàm hỗ trợ để tránh lỗi 'no attribute' nếu controller gọi tên này"""
        self.load_data()