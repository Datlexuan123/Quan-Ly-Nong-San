import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QMessageBox, 
    QFrame, QScrollArea, QWidget, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt

class NvThanhToanView(QDialog):
    def __init__(self, total_amount, cart_data, parent=None):
        super().__init__(parent)
        self.total_amount = total_amount
        self.cart_data = cart_data
        self.discount = 0
        self.customer_id = None
        self.points_used = 0
        # Lấy ID nhân viên từ thông tin đăng nhập nếu có
        self.id_nv = 1
        if parent and hasattr(parent, 'user_data') and parent.user_data:
            self.id_nv = parent.user_data.get('id', 1)
            
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Xác nhận thanh toán & Phân loại đơn hàng")
        self.setFixedSize(950, 750)
        self.setStyleSheet("background-color: #f8f9fa; font-family: 'Segoe UI', Arial;")
        
        main_layout = QHBoxLayout(self)
        
        # --- BÊN TRÁI: PHÂN LOẠI ĐƠN HÀNG ---
        left_frame = QFrame()
        left_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #dee2e6;")
        left_layout = QVBoxLayout(left_frame)
        
        left_layout.addWidget(QLabel("<h3>🧾 Hình thức nhận hàng</h3>"))
        
        # Group chọn loại đơn
        type_group = QFrame()
        type_group.setStyleSheet("background-color: #e8f5e9; border-radius: 8px; padding: 15px;")
        type_v = QVBoxLayout(type_group)
        
        self.radio_store = QRadioButton("🏠 Mua tại cửa hàng")
        self.radio_ship = QRadioButton("🛵 Giao hàng tận nơi (Ship)")
        self.radio_store.setChecked(True) # Mặc định
        
        self.bg_type = QButtonGroup()
        self.bg_type.addButton(self.radio_store)
        self.bg_type.addButton(self.radio_ship)
        
        type_v.addWidget(self.radio_store)
        type_v.addWidget(self.radio_ship)
        
        # Phần nhập địa chỉ (ẩn/hiện dựa trên lựa chọn Ship)
        self.ship_info = QWidget()
        ship_l = QVBoxLayout(self.ship_info)
        ship_l.setContentsMargins(20, 10, 0, 0)
        
        self.txt_address = QLineEdit()
        self.txt_address.setPlaceholderText("Nhập địa chỉ giao hàng cụ thể...")
        self.txt_address.setFixedHeight(35)
        
        self.txt_note = QLineEdit()
        self.txt_note.setPlaceholderText("Ghi chú cho nhân viên giao hàng...")
        self.txt_note.setFixedHeight(35)
        
        ship_l.addWidget(QLabel("Địa chỉ giao hàng:"))
        ship_l.addWidget(self.txt_address)
        ship_l.addWidget(QLabel("Ghi chú ship:"))
        ship_l.addWidget(self.txt_note)
        self.ship_info.setVisible(False)
        
        type_v.addWidget(self.ship_info)
        left_layout.addWidget(type_group)
        left_layout.addStretch()
        
        # --- BÊN PHẢI: CHI TIẾT THANH TOÁN ---
        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #dee2e6;")
        right_layout = QVBoxLayout(right_frame)
        
        right_layout.addWidget(QLabel("<h3>💳 Thanh toán</h3>"))
        
        # Hiển thị số tiền
        money_layout = QVBoxLayout()
        self.lbl_total = QLabel(f"Tổng tiền món: {self.total_amount:,.0f} đ")
        self.lbl_final = QLabel(f"THÀNH TIỀN: {self.total_amount:,.0f} đ")
        self.lbl_final.setStyleSheet("font-size: 22px; font-weight: bold; color: #d32f2f; margin: 10px 0;")
        money_layout.addWidget(self.lbl_total)
        money_layout.addWidget(self.lbl_final)
        right_layout.addLayout(money_layout)

        # Phương thức thanh toán (Tự động lọc)
        right_layout.addWidget(QLabel("<b>Phương thức thanh toán:</b>"))
        self.cbo_method = QComboBox()
        self.cbo_method.setFixedHeight(40)
        self.cbo_method.setStyleSheet("padding-left: 10px; border: 1px solid #ccc;")
        right_layout.addWidget(self.cbo_method)
        
        right_layout.addStretch()
        
        self.btn_finish = QPushButton("✅ HOÀN TẤT THANH TOÁN")
        self.btn_finish.setFixedHeight(55)
        self.btn_finish.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_finish.setStyleSheet("""
            QPushButton { background-color: #2e7d32; color: white; font-size: 16px; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #1b5e20; }
        """)
        self.btn_finish.clicked.connect(self.handle_finish_payment)
        right_layout.addWidget(self.btn_finish)
        
        main_layout.addWidget(left_frame, 1)
        main_layout.addWidget(right_frame, 1)

        # Kết nối sự kiện
        self.radio_store.toggled.connect(self.update_payment_methods)
        self.radio_ship.toggled.connect(self.update_payment_methods)
        self.radio_ship.toggled.connect(lambda c: self.ship_info.setVisible(c))
        
        # Khởi tạo danh sách phương thức lần đầu
        self.update_payment_methods()

    def update_payment_methods(self):
        """Lọc phương thức thanh toán dựa trên loại đơn hàng"""
        self.cbo_method.clear()
        if self.radio_ship.isChecked():
            # Đơn ship chỉ chấp nhận tiền mặt khi nhận hàng hoặc chuyển khoản trước
            self.cbo_method.addItems(["Tiền mặt (COD)", "Chuyển khoản"])
        else:
            # Mua tại quầy có thêm quẹt thẻ
            self.cbo_method.addItems(["Tiền mặt", "Chuyển khoản", "Quẹt thẻ ATM"])

    def handle_finish_payment(self):
        """Xử lý lưu hóa đơn vào cơ sở dữ liệu"""
        # 1. Thu thập dữ liệu từ giao diện
        is_ship = self.radio_ship.isChecked()
        loai_don = 1 if is_ship else 0 # 1: Ship, 0: Tại cửa hàng
        
        addr = self.txt_address.text().strip() if is_ship else ""
        # Kiểm tra nếu chọn ship mà không nhập địa chỉ
        if is_ship and not addr:
            QMessageBox.warning(self, "Chú ý", "Vui lòng nhập địa chỉ giao hàng!")
            return
            
        note = self.txt_note.text().strip() if is_ship else "Mua tại quầy"
        
        # Trạng thái: Ship thì 'Chờ xác nhận' (0), Tại quầy thì 'Đã giao' (2)
        stt_giao = 0 if is_ship else 2 
        
        pt_thanh_toan = self.cbo_method.currentText()
        
        # 2. Gọi Controller để lưu
        from controllers.nv_banhang_controller import NvBanHangController
        ctrl = NvBanHangController()
        
        # Tính toán điểm (giả sử 10k được 1 điểm)
        points_earned = int(self.total_amount / 10000)
        
        success, msg = ctrl.save_invoice(
            cart_data=self.cart_data, 
            total=self.total_amount, 
            customer_id=self.customer_id, 
            id_nv=self.id_nv, 
            points_used=self.points_used, 
            points_earned=points_earned,
            loai_don_hang=loai_don, 
            dia_chi_giao=addr, 
            trang_thai_giao=stt_giao, 
            ghi_chu=note, 
            phuong_thuc=pt_thanh_toan # Tham số mới
        )
        
        if success:
            QMessageBox.information(self, "Thành công", f"Đã lưu đơn hàng thành công!\nLoại đơn: {'Giao hàng' if is_ship else 'Tại chỗ'}")
            self.accept()
        else:
            QMessageBox.warning(self, "Lỗi", f"Không thể lưu hóa đơn: {msg}")