import os
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QGridLayout, QFrame, QScrollArea, QComboBox, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from views.nv.nv_thanhtoan_view import NvThanhToanView
from controllers.nv_banhang_controller import NvBanHangController

class NvBanHangView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = NvBanHangController()
        self.cart_data = {}
        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # --- BÊN TRÁI: DANH SÁCH SẢN PHẨM ---
        left_layout = QVBoxLayout()
        
        # Thanh tìm kiếm & Lọc
        filter_row = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Tìm theo mã hoặc tên sản phẩm...")
        self.txt_search.setFixedHeight(40)
        self.txt_search.setStyleSheet("border: 1px solid #ddd; border-radius: 20px; padding-left: 15px;")
        self.txt_search.textChanged.connect(self.filter_products)

        self.cbo_danhmuc = QComboBox()
        self.cbo_danhmuc.addItem("Tất cả danh mục")
        self.cbo_danhmuc.setFixedSize(150, 40)
        self.cbo_danhmuc.currentTextChanged.connect(self.filter_products)

        filter_row.addWidget(self.txt_search)
        filter_row.addWidget(self.cbo_danhmuc)
        left_layout.addLayout(filter_row)

        # Grid sản phẩm cuộn được
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background-color: #f5f5f5;")
        self.product_container = QWidget()
        self.grid = QGridLayout(self.product_container)
        self.grid.setSpacing(15)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.scroll.setWidget(self.product_container)
        left_layout.addWidget(self.scroll)

        main_layout.addLayout(left_layout, stretch=3)

        # --- BÊN PHẢI: GIỎ HÀNG ---
        cart_frame = QFrame()
        cart_frame.setFixedWidth(350)
        cart_frame.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #e0e0e0;")
        cart_layout = QVBoxLayout(cart_frame)

        self.lbl_cart_header = QLabel("🛒 GIỎ HÀNG")
        self.lbl_cart_header.setStyleSheet("font-weight: bold; font-size: 16px; color: #2e7d32; border:none;")
        self.lbl_cart_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet("border: none;")
        self.cart_items_widget = QWidget()
        self.cart_items_layout = QVBoxLayout(self.cart_items_widget)
        self.cart_items_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cart_scroll.setWidget(self.cart_items_widget)

        # Phần tổng tiền thu nhỏ lại
        summary_layout = QVBoxLayout()
        self.lbl_total = QLabel("Tổng cộng: 0 đ")
        self.lbl_total.setStyleSheet("font-size: 18px; font-weight: bold; color: #d32f2f; border: none;")
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.btn_thanhtoan = QPushButton("THANH TOÁN")
        self.btn_thanhtoan.setFixedHeight(45)
        self.btn_thanhtoan.setStyleSheet("background-color: #2e7d32; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_thanhtoan.clicked.connect(self.handle_payment)

        cart_layout.addWidget(self.lbl_cart_header)
        cart_layout.addWidget(self.cart_scroll)
        cart_layout.addWidget(self.lbl_total)
        cart_layout.addWidget(self.btn_thanhtoan)

        main_layout.addWidget(cart_frame)

    def create_product_card(self, p):
        """ Tạo thẻ sản phẩm giống hệt như ảnh bạn gửi """
        card = QFrame()
        card.setFixedSize(220, 320)
        card.setStyleSheet("""
            QFrame { background-color: white; border: 1px solid #ddd; border-radius: 10px; }
            QFrame:hover { border: 2px solid #4caf50; }
        """)
        v_layout = QVBoxLayout(card)
        v_layout.setContentsMargins(10, 10, 10, 10)

        # Ảnh
        lbl_img = QLabel()
        lbl_img.setFixedSize(200, 150)
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path = p.get("hinh_anh", "")
        if path and os.path.exists(path):
            lbl_img.setPixmap(QPixmap(path).scaled(180, 140, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            lbl_img.setText("📷 No Image")
            lbl_img.setStyleSheet("color: #999; border: none;")
        
        # Tên sản phẩm
        lbl_name = QLabel(p["ten_sp"])
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_name.setStyleSheet("font-weight: bold; font-size: 14px; border: none; padding: 5px;")

        # Giá
        lbl_price = QLabel(f"{float(p['gia_ban']):,.0f} đ")
        lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_price.setStyleSheet("color: #2e7d32; font-weight: bold; font-size: 15px; border: none;")

        # Nút thêm vào giỏ
        btn_add = QPushButton("THÊM VÀO GIỎ")
        btn_add.setFixedHeight(35)
        btn_add.setStyleSheet("background-color: #81c784; color: white; font-weight: bold; border-radius: 5px;")
        btn_add.clicked.connect(lambda _, prod=p: self.add_to_cart(prod))

        v_layout.addWidget(lbl_img)
        v_layout.addWidget(lbl_name)
        v_layout.addWidget(lbl_price)
        v_layout.addWidget(btn_add)
        return card

    def add_to_cart(self, product):
        p_id = product["id"]
        if p_id in self.cart_data:
            self.cart_data[p_id]["qty"] += 1
        else:
            self.cart_data[p_id] = {"info": product, "qty": 1}
        self.refresh_cart_display()

    def refresh_cart_display(self):
        """ Làm mới giỏ hàng với x1, x2 và nút tăng giảm """
        for i in reversed(range(self.cart_items_layout.count())):
            self.cart_items_layout.itemAt(i).widget().setParent(None)

        total_all = 0
        for p_id, item in self.cart_data.items():
            info = item["info"]
            qty = item["qty"]
            subtotal = float(info["gia_ban"]) * qty
            total_all += subtotal

            item_frame = QFrame()
            item_frame.setStyleSheet("background-color: #f9f9f9; border-radius: 5px; border: 1px solid #eee;")
            h_layout = QHBoxLayout(item_frame)
            
            lbl_name = QLabel(f"<b>{info['ten_sp']}</b><br>{float(info['gia_ban']):,.0f}đ")
            lbl_name.setStyleSheet("border: none; font-size: 11px;")
            
            # Cụm nút x1, x2 tăng giảm
            qty_layout = QHBoxLayout()
            btn_sub = QPushButton("-"); btn_sub.setFixedSize(20, 20)
            btn_sub.setStyleSheet("background-color: #e0e0e0; border-radius: 10px; font-weight: bold;")
            btn_sub.clicked.connect(lambda _, id=p_id: self.update_qty(id, -1))

            lbl_qty = QLabel(f"x{qty}")
            lbl_qty.setStyleSheet("font-weight: bold; border: none;")

            btn_plus = QPushButton("+"); btn_plus.setFixedSize(20, 20)
            btn_plus.setStyleSheet("background-color: #e0e0e0; border-radius: 10px; font-weight: bold;")
            btn_plus.clicked.connect(lambda _, id=p_id: self.update_qty(id, 1))

            qty_layout.addWidget(btn_sub); qty_layout.addWidget(lbl_qty); qty_layout.addWidget(btn_plus)

            h_layout.addWidget(lbl_name, stretch=1)
            h_layout.addLayout(qty_layout)
            self.cart_items_layout.addWidget(item_frame)

        self.lbl_total.setText(f"Tổng cộng: {total_all:,.0f} đ")

    def update_qty(self, p_id, delta):
        if p_id in self.cart_data:
            self.cart_data[p_id]["qty"] += delta
            if self.cart_data[p_id]["qty"] <= 0:
                del self.cart_data[p_id]
            self.refresh_cart_display()

    def handle_payment(self):
        if not self.cart_data:
            QMessageBox.warning(self, "Chú ý", "Giỏ hàng đang trống!")
            return

        total = sum(item['qty'] * float(item['info']['gia_ban']) for item in self.cart_data.values())
        
        # Mở dialog thanh toán
        dialog = NvThanhToanView(total, self.cart_data, self)
        
        # Nếu nhấn "HOÀN TẤT HÓA ĐƠN" (Accepted)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 1. Xóa giỏ hàng cũ
            self.cart_data.clear()
            self.refresh_cart_display() # <--- ĐÃ SỬA TÊN HÀM Ở ĐÂY
            
            # 2. CẬP NHẬT LẠI DANH SÁCH SẢN PHẨM TRÊN MÀN HÌNH
            # Lấy lại dữ liệu mới nhất từ database (đã bị trừ tồn kho)
            self.all_products = self.controller.get_sanpham()
            
            # Hiển thị lại lên giao diện lưới sản phẩm
            self.display_products(self.all_products)

    def load_initial_data(self):
        self.all_products = self.controller.get_sanpham()
        self.display_products(self.all_products)
        # Load danh mục
        dm_ids = sorted(list(set(str(p["id_danh_muc"]) for p in self.all_products if p.get("id_danh_muc"))))
        for dm in dm_ids: self.cbo_danhmuc.addItem(f"Danh mục {dm}")

    def display_products(self, products):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget: widget.setParent(None)
        row, col = 0, 0
        for p in products:
            self.grid.addWidget(self.create_product_card(p), row, col)
            col += 1
            if col == 4: col = 0; row += 1

    def filter_products(self):
        kw = self.txt_search.text().lower()
        dm = self.cbo_danhmuc.currentText()
        filtered = [p for p in self.all_products if kw in p["ten_sp"].lower() and 
                   (dm == "Tất cả danh mục" or f"Danh mục {p['id_danh_muc']}" == dm)]
        self.display_products(filtered)