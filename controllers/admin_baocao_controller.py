from PyQt6.QtWidgets import QTableWidgetItem

class AdminBaoCaoController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        
        # Kết nối nút làm mới trong View
        self.view.btn_refresh.clicked.connect(self.load_all_reports)
        
        # Load dữ liệu lần đầu
        self.load_all_reports()

    def load_all_reports(self):
        """Hàm tổng để gọi load tất cả các tab"""
        self.load_inventory_and_waste()
        # Lưu ý: Hàm load_revenue_data và load_customer_data 
        # nên được chuyển dần từ View sang Controller này sau.
        self.view.load_revenue_data() 
        self.view.load_customer_data()

    def load_inventory_and_waste(self):
        """Đổ dữ liệu vào tab Kho & Hàng hủy (Đã sửa để hiện hàng hủy thật)"""
        try:
            # 1. Lấy dữ liệu hàng hủy từ model
            canceled_data = self.model.get_canceled_stock()
            
            # 2. Cập nhật bảng table_inventory trong View
            # Chỉnh lại tiêu đề cột cho khớp với hàng hủy
            self.view.table_inventory.setColumnCount(5)
            self.view.table_inventory.setHorizontalHeaderLabels([
                "ID", "Sản Phẩm", "SL Hủy", "Ngày Hủy", "Lý Do"
            ])
            
            self.view.table_inventory.setRowCount(0)
            for r in canceled_data:
                row = self.view.table_inventory.rowCount()
                self.view.table_inventory.insertRow(row)
                self.view.table_inventory.setItem(row, 0, QTableWidgetItem(str(r['id'])))
                self.view.table_inventory.setItem(row, 1, QTableWidgetItem(str(r['ten_sp'])))
                self.view.table_inventory.setItem(row, 2, QTableWidgetItem(str(r['so_luong_huy'])))
                self.view.table_inventory.setItem(row, 3, QTableWidgetItem(str(r['ngay_huy'])))
                self.view.table_inventory.setItem(row, 4, QTableWidgetItem(str(r['ly_do'])))
        except Exception as e:
            print(f"Lỗi tại Controller báo cáo: {e}")