from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton
from models.hoadon_model import HoaDonModel
from views.nv.order_edit_dialog import OrderEditDialog

class NvDonHangController:
    def __init__(self, view, user_data=None):
        self.view = view
        self.user_data = user_data # Thông tin nhân viên đăng nhập
        self.model = HoaDonModel()
        
        # 1. Kết nối các nút bấm trên giao diện
        self.view.btn_refresh.clicked.connect(self.load_data)
        self.view.cb_status.currentIndexChanged.connect(self.load_data)
        
        # 2. KẾT NỐI NÚT THÊM ĐƠN HÀNG (Sửa lỗi bạn đang gặp)
        if hasattr(self.view, 'btn_add'):
            self.view.btn_add.clicked.connect(self.handle_add_order)
        
        # Mặc định load dữ liệu khi khởi chạy
        self.load_data()

    def handle_add_order(self):
        """Xử lý khi nhấn nút Thêm đơn hàng: Chuyển hướng sang tab Bán hàng"""
        # Tìm cửa sổ chính (NvMainView) để gọi hàm chuyển page
        parent = self.view.window() 
        if hasattr(parent, 'btn_banhang'):
            # Giả lập hành động nhấn vào nút Bán hàng trên Sidebar
            parent.btn_banhang.click()
        else:
            QMessageBox.information(self.view, "Thông báo", 
                "Vui lòng chọn mục '🛒 Bán hàng' ở thanh bên trái để tạo đơn mới!")

    def load_data(self):
        # Lấy index trạng thái từ ComboBox (-1 là "Tất cả")
        status_idx = self.view.cb_status.currentIndex() - 1
        
        # CHỈ LẤY ĐƠN SHIP (loai_don_hang = 1)
        orders = self.model.get_orders_by_type(is_ship=True, status=status_idx if status_idx >= 0 else -1)
        
        # Thống kê đơn cần xử lý (Trạng thái 0 và 1)
        pending_count = sum(1 for o in orders if o['trang_thai_giao'] in [0, 1])
        self.view.lbl_stats.setText(f"🚚 Đơn ship cần xử lý: {pending_count}")
        
        self.view.table.setRowCount(0)
        for row, order in enumerate(orders):
            self.view.table.insertRow(row)
            self.view.table.setItem(row, 0, QTableWidgetItem(str(order['id'])))
            self.view.table.setItem(row, 1, QTableWidgetItem(str(order['ngay_lap'])))
            self.view.table.setItem(row, 2, QTableWidgetItem(order['ten_khach'] or "Khách lẻ"))
            self.view.table.setItem(row, 3, QTableWidgetItem(order['dia_chi_giao'] or "Chưa có địa chỉ"))
            self.view.table.setItem(row, 4, QTableWidgetItem(f"{order['tong_tien']:,} đ"))
            
            # Trạng thái bằng chữ kèm Icon
            stt_text = self.get_status_label(order['trang_thai_giao'])
            self.view.table.setItem(row, 5, QTableWidgetItem(stt_text))
            
            # Cột Thao tác
            self.add_action_buttons(row, order)

    def get_status_label(self, s):
        labels = {0: "⏳ Chờ xác nhận", 1: "🛵 Đang giao", 2: "✅ Đã giao", 3: "❌ Đã hủy"}
        return labels.get(s, "Không xác định")

    def add_action_buttons(self, row, order):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)

        # Nút Sửa địa chỉ (Lưu lịch sử)
        btn_edit = QPushButton("📍 Sửa địa chỉ")
        btn_edit.setStyleSheet("background-color: #fbc02d; color: black; font-weight: bold; padding: 5px;")
        btn_edit.clicked.connect(lambda: self.open_edit_dialog(order))

        # Nút Cập nhật trạng thái
        btn_step = QPushButton("➡️ Tiến độ")
        btn_step.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; padding: 5px;")
        btn_step.clicked.connect(lambda: self.next_step_status(order))
        
        # Khóa nút nếu đơn đã hoàn tất hoặc bị hủy
        if order['trang_thai_giao'] >= 2:
            btn_step.setEnabled(False)
            btn_step.setStyleSheet("background-color: #bdc3c7; color: white;")

        layout.addWidget(btn_edit)
        layout.addWidget(btn_step)
        self.view.table.setCellWidget(row, 6, container)

    def open_edit_dialog(self, order):
        dialog = OrderEditDialog(order)
        if dialog.exec():
            new_address = dialog.get_data()
            # Lấy tên nhân viên đang thao tác từ user_data
            editor_name = self.user_data.get('ho_ten', 'Nhân viên') if self.user_data else "Nhân viên"
            
            if self.model.update_order_info(order['id'], new_address, editor_name):
                QMessageBox.information(self.view, "Thành công", f"Đã cập nhật địa chỉ và lưu vết bởi {editor_name}!")
                self.load_data()

    def next_step_status(self, order):
        current_stt = order['trang_thai_giao']
        if current_stt < 2: 
            new_stt = current_stt + 1
            if self.model.update_status(order['id'], new_stt):
                self.load_data()