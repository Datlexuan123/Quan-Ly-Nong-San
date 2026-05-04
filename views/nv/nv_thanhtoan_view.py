import os
import qrcode
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QMessageBox, 
    QFrame, QWidget, QRadioButton, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class NvThanhToanView(QDialog):
    def __init__(self, total_amount, cart_data, parent=None):
        super().__init__(parent)
        self.original_total = total_amount
        self.total_amount = total_amount
        self.cart_data = cart_data # Chứa thông tin mặt hàng từ giỏ hàng
        self.customer_id = None
        self.points_available = 0
        self.points_used = 0
        self.id_nv = 1
        
        if parent and hasattr(parent, 'user_data') and parent.user_data:
            self.id_nv = parent.user_data.get('id', 1)
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Xác nhận thanh toán")
        self.setFixedSize(1000, 750) 
        self.setStyleSheet("background-color: #f8f9fa; font-family: 'Segoe UI', Arial;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        body_layout = QHBoxLayout()
        
        # --- CỘT TRÁI: KHÁCH HÀNG & GIAO HÀNG ---
        left_col = QVBoxLayout()
        
        # 1. Khu vực Khách hàng & Điểm
        cust_group = QGroupBox("👤 Thông tin khách hàng & Điểm")
        cust_group.setStyleSheet("QGroupBox { font-weight: bold; color: #2e7d32; border: 1px solid #ccc; margin-top: 10px; padding: 10px; }")
        cust_layout = QVBoxLayout(cust_group)
        
        phone_row = QHBoxLayout()
        self.txt_phone = QLineEdit()
        self.txt_phone.setPlaceholderText("Số điện thoại...")
        self.txt_phone.setFixedHeight(35)
        self.btn_search = QPushButton("Tìm")
        self.btn_search.setFixedWidth(60)
        self.btn_search.setStyleSheet("background-color: #0d6efd; color: white; font-weight: bold;")
        self.btn_search.clicked.connect(self.handle_search_customer)
        phone_row.addWidget(self.txt_phone)
        phone_row.addWidget(self.btn_search)
        cust_layout.addLayout(phone_row)
        
        self.txt_cust_name = QLineEdit()
        self.txt_cust_name.setPlaceholderText("Họ tên khách hàng")
        self.txt_cust_name.setFixedHeight(35)
        cust_layout.addWidget(self.txt_cust_name)
        
        point_row = QHBoxLayout()
        self.lbl_points = QLabel("Điểm hiện có: 0")
        self.lbl_points.setStyleSheet("color: blue; font-weight: bold;")
        self.txt_use_point = QLineEdit()
        self.txt_use_point.setPlaceholderText("Nhập điểm dùng...")
        self.txt_use_point.setFixedWidth(120)
        self.btn_apply_point = QPushButton("Dùng điểm")
        self.btn_apply_point.clicked.connect(self.apply_points_logic)
        
        point_row.addWidget(self.lbl_points)
        point_row.addStretch()
        point_row.addWidget(self.txt_use_point)
        point_row.addWidget(self.btn_apply_point)
        cust_layout.addLayout(point_row)
        left_col.addWidget(cust_group)
        
        # 2. Khu vực Nhận hàng
        ship_group = QGroupBox("🚚 Hình thức nhận hàng")
        ship_group.setStyleSheet("QGroupBox { font-weight: bold; color: #1976d2; border: 1px solid #ccc; margin-top: 10px; padding: 10px; }")
        ship_layout = QVBoxLayout(ship_group)
        self.radio_store = QRadioButton("Mua trực tiếp tại cửa hàng")
        self.radio_ship = QRadioButton("Giao hàng tận nơi (Ship)")
        self.radio_store.setChecked(True)
        self.txt_ship_addr = QLineEdit()
        self.txt_ship_addr.setPlaceholderText("Nhập địa chỉ giao hàng...")
        self.txt_ship_addr.setFixedHeight(35)
        self.txt_ship_addr.setVisible(False)
        ship_layout.addWidget(self.radio_store)
        ship_layout.addWidget(self.radio_ship)
        ship_layout.addWidget(self.txt_ship_addr)
        self.radio_ship.toggled.connect(self.txt_ship_addr.setVisible)
        left_col.addWidget(ship_group)
        
        body_layout.addLayout(left_col, 4)
        
        # --- CỘT PHẢI: CHI TIẾT MẶT HÀNG & THANH TOÁN ---
        right_col = QVBoxLayout()
        
        # 3. Bảng danh sách mặt hàng (MỚI THÊM)
        item_group = QGroupBox("🛒 Danh sách mặt hàng")
        item_group.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid #ccc; margin-top: 10px; padding: 5px; }")
        item_layout = QVBoxLayout(item_group)
        
        self.table_items = QTableWidget()
        self.table_items.setColumnCount(3)
        self.table_items.setHorizontalHeaderLabels(["Tên hàng", "SL", "Thành tiền"])
        self.table_items.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_items.setFixedHeight(200) # Giới hạn chiều cao bảng
        self.load_cart_to_table() # Gọi hàm đổ dữ liệu vào bảng
        item_layout.addWidget(self.table_items)
        right_col.addWidget(item_group)

        # 4. Thông tin tiền & Phương thức
        pay_group = QGroupBox("💳 Thanh toán")
        pay_group.setStyleSheet("QGroupBox { font-weight: bold; color: #d32f2f; border: 1px solid #ccc; padding: 10px; }")
        pay_layout = QVBoxLayout(pay_group)
        
        self.lbl_total_display = QLabel(f"TỔNG CỘNG: {self.total_amount:,.0f} đ")
        self.lbl_total_display.setStyleSheet("font-size: 24px; font-weight: bold; color: red;")
        pay_layout.addWidget(self.lbl_total_display)
        
        self.cbo_method = QComboBox()
        self.cbo_method.addItems(["Tiền mặt", "Chuyển khoản"])
        self.cbo_method.setFixedHeight(35)
        self.cbo_method.currentTextChanged.connect(self.update_qr)
        pay_layout.addWidget(QLabel("<b>Phương thức:</b>"))
        pay_layout.addWidget(self.cbo_method)
        
        self.qr_label = QLabel()
        self.qr_label.setFixedSize(150, 150)
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setStyleSheet("border: 1px dashed #bbb; background: white;")
        self.qr_label.setVisible(False)
        pay_layout.addWidget(self.qr_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        right_col.addWidget(pay_group)
        body_layout.addLayout(right_col, 6)
        
        main_layout.addLayout(body_layout)
        
        # Nút xác nhận
        self.btn_confirm = QPushButton("✅ HOÀN TẤT THANH TOÁN")
        self.btn_confirm.setFixedHeight(60)
        self.btn_confirm.setStyleSheet("background-color: #198754; color: white; font-size: 18px; font-weight: bold; border-radius: 8px;")
        self.btn_confirm.clicked.connect(self.handle_finish_payment)
        main_layout.addWidget(self.btn_confirm)

    def load_cart_to_table(self):
        """Đổ dữ liệu từ cart_data vào bảng hiển thị"""
        self.table_items.setRowCount(len(self.cart_data))
        row = 0
        for p_id, item in self.cart_data.items():
            # Lấy tên sản phẩm dựa trên cột 'ten_sp' trong database của bạn
            name = item['info'].get('ten_sp', 'Sản phẩm không tên')
            qty = item['qty']
            price = float(item['info'].get('gia_ban', 0))
            
            # Tính thành tiền cho dòng này
            line_total = qty * price
            
            # Đổ dữ liệu vào các cột của bảng QTableWidget
            self.table_items.setItem(row, 0, QTableWidgetItem(name))
            self.table_items.setItem(row, 1, QTableWidgetItem(str(qty)))
            self.table_items.setItem(row, 2, QTableWidgetItem(f"{line_total:,.0f}"))
            row += 1

    # --- CÁC HÀM XỬ LÝ LOGIC (Giữ nguyên) ---
    def handle_search_customer(self):
        sdt = self.txt_phone.text().strip()
        if not sdt: return
        from controllers.nv_banhang_controller import NvBanHangController
        ctrl = NvBanHangController()
        kh = ctrl.get_customer_by_phone(sdt)
        if kh:
            self.customer_id = kh['id']
            self.txt_cust_name.setText(kh['ho_ten'])
            self.points_available = kh.get('diem_tich_luy', 0)
            self.lbl_points.setText(f"Điểm hiện có: {self.points_available}")
            self.txt_ship_addr.setText(kh.get('dia_chi', ''))
        else:
            self.customer_id = None
            self.lbl_points.setText("Khách mới (0 điểm)")

    def apply_points_logic(self):
        try:
            val = int(self.txt_use_point.text() or 0)
            if val > self.points_available:
                QMessageBox.warning(self, "Lỗi", "Không đủ điểm!")
                return
            self.points_used = val
            discount = val * 1000 
            self.total_amount = self.original_total - discount
            if self.total_amount < 0: self.total_amount = 0
            self.lbl_total_display.setText(f"TỔNG CỘNG: {self.total_amount:,.0f} đ")
            QMessageBox.information(self, "Xong", f"Đã dùng {val} điểm. Giảm: {discount:,.0f} đ")
        except:
            QMessageBox.warning(self, "Lỗi", "Nhập số điểm hợp lệ!")

    def update_qr(self, method):
        if method == "Chuyển khoản":
            qr = qrcode.make(f"STK: 123456 - So tien: {self.total_amount}")
            qr.save("pay.png")
            self.qr_label.setPixmap(QPixmap("pay.png").scaled(150, 150))
            self.qr_label.setVisible(True)
        else:
            self.qr_label.setVisible(False)

    def handle_finish_payment(self):
        sdt = self.txt_phone.text().strip()
        ten = self.txt_cust_name.text().strip()
        if not sdt or not ten:
            QMessageBox.warning(self, "Lỗi", "Thiếu SĐT hoặc Tên khách!")
            return
        
        # Kiểm tra hình thức nhận hàng
        is_ship = self.radio_ship.isChecked()
        addr = self.txt_ship_addr.text().strip() if is_ship else "Mua tại quầy"
        
        # LOGIC MỚI: Định nghĩa trạng thái giao hàng
        # Nếu là Ship -> Trạng thái 0 (Chờ xử lý)
        # Nếu mua tại quầy -> Trạng thái 2 (Đã giao)
        trang_thai = 0 if is_ship else 2 

        from controllers.nv_banhang_controller import NvBanHangController
        ctrl = NvBanHangController()
        points_earned = int(self.total_amount / 20000)

        success, msg = ctrl.save_invoice(
            self.cart_data, 
            self.total_amount, 
            self.customer_id, 
            self.id_nv,
            self.points_used, 
            points_earned, 
            (1 if is_ship else 0), # Loại đơn hàng (1: Ship, 0: Tại quầy)
            addr, 
            trang_thai, # SỬA TẠI ĐÂY: Thay con số 2 bằng biến trang_thai
            "", 
            self.cbo_method.currentText(), 
            sdt, 
            ten
        )
        if success: self.accept()
        else: QMessageBox.critical(self, "Lỗi", msg)