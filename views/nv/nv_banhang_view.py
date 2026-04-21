import os
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QGridLayout, QFrame, QScrollArea, QComboBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

# Kết nối với Controller thực tế của bạn
from controllers.nv_banhang_controller import NvBanHangController

class NvBanHangView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Bán Hàng Nông Sản")
        self.resize(1150, 750)

        self.controller = NvBanHangController()
        # Lưu trữ giỏ hàng: { id_sp: {"info": p, "qty": số_lượng} }
        self.cart_data = {}

        # Layout chính
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # ==========================================================
        # PHẦN BÊN TRÁI: DANH SÁCH SẢN PHẨM
        # ==========================================================
        left_container = QVBoxLayout()

        # Thanh tìm kiếm & Bộ lọc
        search_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Tìm theo mã hoặc tên sản phẩm...")
        self.txt_search.setFixedHeight(40)
        self.txt_search.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 20px;
                padding-left: 15px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus { border: 1px solid #78c257; }
        """)

        self.cbo_danhmuc = QComboBox()
        self.cbo_danhmuc.addItem("Tất cả danh mục")
        self.cbo_danhmuc.setFixedSize(160, 40)

        search_layout.addWidget(self.txt_search)
        search_layout.addWidget(self.cbo_danhmuc)
        left_container.addLayout(search_layout)

        # Vùng cuộn chứa Grid sản phẩm
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.product_widget = QWidget()
        self.product_widget.setStyleSheet("background-color: #f5f5f5;")
        self.grid = QGridLayout(self.product_widget)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.scroll.setWidget(self.product_widget)
        left_container.addWidget(self.scroll)

        main_layout.addLayout(left_container, stretch=3)

        # ==========================================================
        # PHẦN BÊN PHẢI: GIỎ HÀNG (CÓ NÚT +/- VÀ X1 X2)
        # ==========================================================
        cart_frame = QFrame()
        cart_frame.setFixedWidth(20)
        cart_frame.setStyleSheet("background-color: white; border-radius: 15px; border: 1px solid #ddd;")
        
        cart_layout = QVBoxLayout(cart_frame)

        self.lbl_cart_header = QLabel("🛒 GIỎ HÀNG")
        self.lbl_cart_header.setStyleSheet("font-weight: bold; font-size: 15px; color: #333; border:none; padding: 5px;")
        self.lbl_cart_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cart_scroll = QScrollArea()
        self.cart_scroll.setWidgetResizable(True)
        self.cart_scroll.setStyleSheet("border: none; background: white;")
        
        self.cart_container = QWidget()
        self.cart_items_layout = QVBoxLayout(self.cart_container)
        self.cart_items_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cart_items_layout.setContentsMargins(5, 5, 5, 5)
        self.cart_items_layout.setSpacing(10)
        self.cart_scroll.setWidget(self.cart_container)

        self.lbl_total = QLabel("Tổng cộng: 0 đ")
        self.lbl_total.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c; border:none; padding: 10px 0;")

        self.btn_thanhtoan = QPushButton("THANH TOÁN NGAY")
        self.btn_thanhtoan.setFixedHeight(50)
        self.btn_thanhtoan.setStyleSheet("""
            QPushButton {
                background-color: #78c257;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                font-size: 10px;
            }
            QPushButton:hover { background-color: #66a34a; }
        """)

        cart_layout.addWidget(self.lbl_cart_header)
        cart_layout.addWidget(self.cart_scroll)
        cart_layout.addWidget(self.lbl_total)
        cart_layout.addWidget(self.btn_thanhtoan)

        main_layout.addWidget(cart_frame, stretch=1)

        # ===== KHỞI CHẠY DỮ LIỆU =====
        self.all_products = self.controller.get_sanpham()
        self.load_danhmuc()
        self.display_products(self.all_products)

        # ===== SỰ KIỆN =====
        self.txt_search.textChanged.connect(self.filter_products)
        self.cbo_danhmuc.currentTextChanged.connect(self.filter_products)

    def load_danhmuc(self):
        danh_muc_set = set(str(p["id_danh_muc"]) for p in self.all_products if p.get("id_danh_muc"))
        for dm in sorted(danh_muc_set):
            self.cbo_danhmuc.addItem(f"Danh mục {dm}")

    def display_products(self, products):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget: widget.setParent(None)

        row, col = 0, 0
        for p in products:
            card = self.create_product_card(p)
            self.grid.addWidget(card, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1

    def create_product_card(self, p):
        card = QFrame()
        card.setFixedSize(185, 285)
        card.setObjectName("productCard")
        card.setStyleSheet("""
            #productCard { background-color: white; border: 1px solid #e0e0e0; border-radius: 12px; }
            #productCard:hover { border: 2px solid #78c257; }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(5, 5, 5, 10)

        # Ảnh sản phẩm
        lbl_img = QLabel()
        lbl_img.setFixedSize(170, 140)
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Đường dẫn ảnh dựa trên cấu trúc dự án của bạn
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.abspath(os.path.join(base_dir, "..", ".."))
        image_path = os.path.join(project_dir, p["hinh_anh"]) if p["hinh_anh"] else ""

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            lbl_img.setPixmap(pixmap.scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            lbl_img.setText("📷 No Image")
            lbl_img.setStyleSheet("color: #bbb; font-style: italic;")

        lbl_name = QLabel(p["ten_sp"])
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_name.setStyleSheet("font-weight: bold; font-size: 14px; color: #333; border:none;")

        lbl_price = QLabel(f"{float(p['gia_ban']):,.0f} đ")
        lbl_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_price.setStyleSheet("color: #78c257; font-weight: bold; font-size: 15px; border:none;")

        btn_add = QPushButton("THÊM VÀO GIỎ")
        btn_add.setFixedHeight(30)
        btn_add.setStyleSheet("background-color: #78c257; color: white; border-radius: 4px; font-weight: bold; font-size: 10px;")
        btn_add.clicked.connect(lambda _, prod=p: self.add_to_cart(prod))

        layout.addWidget(lbl_img)
        layout.addWidget(lbl_name)
        layout.addWidget(lbl_price)
        layout.addWidget(btn_add)
        return card

    # ================= LOGIC GIỎ HÀNG =================
    def add_to_cart(self, product):
        p_id = product["id"]
        if p_id in self.cart_data:
            self.cart_data[p_id]["qty"] += 1
        else:
            self.cart_data[p_id] = {"info": product, "qty": 1}
        self.refresh_cart_display()

    def update_qty(self, p_id, delta):
        if p_id in self.cart_data:
            self.cart_data[p_id]["qty"] += delta
            if self.cart_data[p_id]["qty"] <= 0:
                del self.cart_data[p_id]
            self.refresh_cart_display()

    def refresh_cart_display(self):
        for i in reversed(range(self.cart_items_layout.count())):
            widget = self.cart_items_layout.itemAt(i).widget()
            if widget: widget.setParent(None)

        total_all = 0
        for p_id, item in self.cart_data.items():
            info = item["info"]
            qty = item["qty"]
            price = float(info["gia_ban"])
            total_all += price * qty

            row = QFrame()
            row.setStyleSheet("border-bottom: 1px solid #eee; padding: 5px;")
            row_layout = QHBoxLayout(row)

            name_info = QLabel(f"<b>{info['ten_sp']}</b><br><font color='green'>{price:,.0f}đ</font>")
            name_info.setStyleSheet("border:none; font-size: 12px;")

            qty_layout = QHBoxLayout()
            btn_minus = QPushButton("-")
            btn_minus.setFixedSize(20, 20)
            btn_minus.setStyleSheet("background: #f1f1f1; border-radius: 12px; font-weight: bold;")
            btn_minus.clicked.connect(lambda _, id=p_id: self.update_qty(id, -1))

            lbl_qty = QLabel(f"x{qty}")
            lbl_qty.setStyleSheet("font-weight: bold; border: none; min-width: 30px;")
            lbl_qty.setAlignment(Qt.AlignmentFlag.AlignCenter)

            btn_plus = QPushButton("+")
            btn_plus.setFixedSize(25, 25)
            btn_plus.setStyleSheet("background: #f1f1f1; border-radius: 12px; font-weight: bold;")
            btn_plus.clicked.connect(lambda _, id=p_id: self.update_qty(id, 1))

            qty_layout.addWidget(btn_minus)
            qty_layout.addWidget(lbl_qty)
            qty_layout.addWidget(btn_plus)

            row_layout.addWidget(name_info, stretch=1)
            row_layout.addLayout(qty_layout)
            self.cart_items_layout.addWidget(row)

        self.lbl_total.setText(f"Tổng cộng: {total_all:,.0f} đ")

    def filter_products(self):
        keyword = self.txt_search.text().lower()
        danh_muc = self.cbo_danhmuc.currentText()
        filtered = []
        for p in self.all_products:
            match_keyword = keyword in p["ten_sp"].lower() or keyword in str(p["id"])
            match_danhmuc = (danh_muc == "Tất cả danh mục" or f"Danh mục {p['id_danh_muc']}" == danh_muc)
            if match_keyword and match_danhmuc:
                filtered.append(p)
        self.display_products(filtered)