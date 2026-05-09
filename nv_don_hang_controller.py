from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton
from models.hoadon_model import HoaDonModel
from views.nv.order_edit_dialog import OrderEditDialog

class NvDonHangController:
    def __init__(self, view, user_data=None):
        self.view = view
        self.user_data = user_data if user_data else {}
        self.model = HoaDonModel()
        self.view.btn_refresh.clicked.connect(self.load_data)
        self.view.cb_status.currentIndexChanged.connect(self.load_data)
        if hasattr(self.view, 'btn_add'):
            self.view.btn_add.clicked.connect(self.handle_add_order)
        self.load_data()

    def load_data(self):
        status_idx = self.view.cb_status.currentIndex() - 1
        orders = self.model.get_orders_by_type(is_ship=True, status=status_idx if status_idx >= 0 else -1)
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
            self.view.table.setItem(row, 5, QTableWidgetItem(self.get_status_label(order['trang_thai_giao'])))
            self.add_action_buttons(row, order)

    def get_status_label(self, s):
        labels = {0: "⏳ Chờ xác nhận", 1: "🛵 Đang giao", 2: "✅ Đã giao", 3: "❌ Đã hủy"}
        return labels.get(s, "Không xác định")

    def add_action_buttons(self, row, order):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)
        btn_edit = QPushButton("📍 Sửa địa chỉ")
        btn_edit.setStyleSheet("background-color: #fbc02d; color: black; font-weight: bold; padding: 5px;")
        btn_edit.clicked.connect(lambda: self.open_edit_dialog(order))
        btn_step = QPushButton("➡️ Tiến độ")
        btn_step.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; padding: 5px;")
        btn_step.clicked.connect(lambda: self.next_step_status(order))
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
            editor_name = self.user_data.get('ho_ten', 'Nhân viên')
            editor_id = self.user_data.get('id', 1)
            if self.model.update_order_info(order['id'], new_address, editor_name):
                # Ghi log hoạt động sửa địa chỉ[cite: 19]
                self.model.ghi_log(editor_id, f"Đã sửa địa chỉ đơn hàng #{order['id']}")
                QMessageBox.information(self.view, "Thành công", "Đã cập nhật địa chỉ!")
                self.load_data()

    def next_step_status(self, order):
        current_stt = order['trang_thai_giao']
        if current_stt < 2: 
            new_stt = current_stt + 1
            editor_id = self.user_data.get('id', 1)
            if self.model.update_status(order['id'], new_stt):
                # Ghi log hoạt động cập nhật trạng thái[cite: 19]
                stt_text = self.get_status_label(new_stt)
                self.model.ghi_log(editor_id, f"Đã chuyển đơn #{order['id']} sang {stt_text}")
                self.load_data()

    def handle_add_order(self):
        parent = self.view.window() 
        if hasattr(parent, 'btn_banhang'):
            parent.btn_banhang.click()