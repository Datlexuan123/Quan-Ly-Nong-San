# controllers/admin_order_controller.py

from PyQt6.QtWidgets import (
    QTableWidgetItem, QDialog, QVBoxLayout, QTableWidget, 
    QHeaderView, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class AdminOrderController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        # Kết nối sự kiện click vào bảng
        self.view.table.cellClicked.connect(self.handle_cell_click)
        self.load_orders()

   # controllers/admin_order_controller.py

    def load_orders(self):
        try:
            # Lấy tất cả đơn hàng từ model
            orders = self.model.get_all_orders_admin() 
            
            self.view.table.setRowCount(0)
            self.view.table.verticalHeader().setDefaultSectionSize(45)

            for row, o in enumerate(orders):
                self.view.table.insertRow(row)
                
                # --- PHẦN SỬA ĐỔI: Hiện số thứ tự từ 1 ---
                # Dùng row + 1 để hiện 1, 2, 3...
                item_stt = QTableWidgetItem(str(row + 1))
                item_stt.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_stt.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                
                # QUAN TRỌNG: Lưu ID thật vào Data của Item để khi click vẫn lấy được ID
                item_stt.setData(Qt.ItemDataRole.UserRole, o['id']) 
                
                self.view.table.setItem(row, 0, item_stt)

                # 1. Ngày lập
                ngay_lap = o['ngay_lap'].strftime("%d/%m/%Y %H:%M") if o['ngay_lap'] else "N/A"
                self.view.table.setItem(row, 1, QTableWidgetItem(ngay_lap))
                
                # 2. Khách hàng
                ten_khach = o.get('ten_khach') or "Khách vãng lai"
                self.view.table.setItem(row, 2, QTableWidgetItem(ten_khach))
                
                # 3. Loại đơn (Tại quầy / Giao hàng)
                loai_val = o.get('loai_don_hang', 0)
                loai_text = "Giao hàng" if loai_val == 1 else "Tại quầy"
                item_loai = QTableWidgetItem(loai_text)
                if loai_val == 1:
                    item_loai.setForeground(QColor("#1976d2"))
                else:
                    item_loai.setForeground(QColor("#388e3c"))
                self.view.table.setItem(row, 3, item_loai)

                # 4. Tổng tiền
                tong_tien = float(o.get('tong_tien') or 0)
                self.view.table.setItem(row, 4, QTableWidgetItem(f"{tong_tien:,.0f} đ"))
                
                # 5. Trạng thái
                tt_text = self.get_status_text(o.get('trang_thai_giao'), loai_val)
                self.view.table.setItem(row, 5, QTableWidgetItem(tt_text))
                
        except Exception as e:
            print(f"Lỗi hiển thị danh sách đơn: {e}")

    def get_status_text(self, status, loai_don):
        if loai_don == 0: # Tại quầy
            return "✅ Hoàn thành"
        
        # Đơn giao hàng
        mapping = {0: "⏳ Chờ duyệt", 1: "📦 Đang giao", 2: "✅ Đã giao", 3: "❌ Đã hủy"}
        return mapping.get(status, "Không xác định")

    # controllers/admin_order_controller.py

    def handle_cell_click(self, row, column):
        """Khi click vào bất kỳ ô nào trong hàng, sẽ hiện chi tiết hóa đơn"""
        try:
            # Lấy ID hóa đơn từ cột đầu tiên (cột 0)
            order_id_item = self.view.table.item(row, 0)
            if order_id_item:
                order_id = order_id_item.text()
                # Gọi hàm hiển thị chi tiết
                self.show_order_details(order_id)
        except Exception as e:
            print(f"Lỗi khi xử lý click bảng hóa đơn: {e}")

    def show_order_details(self, order_id):
        """Lấy dữ liệu từ Model và hiện cửa sổ chi tiết"""
        try:
            # 1. Lấy chi tiết từ Model (hàm get_order_details đã có trong hoadon_model.py)
            details = self.model.get_order_details(order_id)
            
            if not details:
                # Nếu không có dữ liệu (có thể do lỗi truy vấn)
                print(f"Không tìm thấy chi tiết cho đơn hàng #{order_id}")
                return

            # 2. Khởi tạo cửa sổ Dialog
            dialog = QDialog(self.view)
            dialog.setWindowTitle(f"CHI TIẾT ĐƠN HÀNG #{order_id}")
            dialog.setMinimumSize(600, 450)
            dialog.setStyleSheet("background-color: white; font-family: Arial;")
            
            layout = QVBoxLayout(dialog)
            
            # Tiêu đề cửa sổ
            title = QLabel(f"DANH SÁCH MÓN HÀNG - ĐƠN #{order_id}")
            title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2e7d32; padding: 10px;")
            layout.addWidget(title)

            # 3. Tạo bảng hiển thị chi tiết
            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(["Sản phẩm", "Số lượng", "Đơn giá", "Thành tiền"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Không cho sửa trực tiếp
            
            table.setRowCount(len(details))
            tong_don = 0
            
            for i, d in enumerate(details):
                table.setItem(i, 0, QTableWidgetItem(str(d.get('ten_sp', 'N/A'))))
                
                sl = d.get('so_luong', 0)
                table.setItem(i, 1, QTableWidgetItem(str(sl)))
                
                gia = float(d.get('don_gia') or 0)
                table.setItem(i, 2, QTableWidgetItem(f"{gia:,.0f} đ"))
                
                thanh_tien = float(d.get('thanh_tien') or 0)
                table.setItem(i, 3, QTableWidgetItem(f"{thanh_tien:,.0f} đ"))
                
                tong_don += thanh_tien

            layout.addWidget(table)
            
            # Hiển thị tổng cộng cuối đơn
            lbl_tong = QLabel(f"TỔNG CỘNG: {tong_don:,.0f} VNĐ")
            lbl_tong.setStyleSheet("font-size: 16px; font-weight: bold; color: red; margin-top: 10px;")
            lbl_tong.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(lbl_tong)

            # Nút đóng
            btn_close = QPushButton("Đóng")
            btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_close.setStyleSheet("background-color: #f5f5f5; padding: 8px; border-radius: 5px;")
            btn_close.clicked.connect(dialog.close)
            layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignRight)
            
            dialog.exec()
            
        except Exception as e:
            print(f"Lỗi hiển thị Dialog chi tiết: {e}")