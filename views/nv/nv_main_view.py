import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt

# ===== IMPORT VIEW =====
from views.nv.nv_banhang_view import NvBanHangView
from views.nv.nv_kho_view import NvKhoView
from views.nv.nv_khach_hang_view import NvKhachHangView 
from controllers.nv_khach_hang_controller import NvKhachHangController

class NvMainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Giao diện nhân viên")
        self.setGeometry(200, 200, 1300, 900)

        # ===== Widget chính =====
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== Sidebar =====
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #2e7d32; color: white;")
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("Nông Sản Sạch")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 25px 10px;")
        sidebar_layout.addWidget(title)

        # Khởi tạo các nút
        self.btn_banhang = self.create_nav_btn("🛒 Bán hàng")
        self.btn_nhaphang = self.create_nav_btn("📦 Kho & Nhập hàng")
        self.btn_kiemkho = self.create_nav_btn("📊 Kiểm kho & báo hủy")
        self.btn_khachhang = self.create_nav_btn("👥 Khách hàng")
        self.btn_nhanvien = self.create_nav_btn("👤 Thông tin NV")
        self.btn_logout = self.create_nav_btn("🚪 Đăng xuất")

        # Thêm các nút chức năng vào layout
        self.buttons = [self.btn_banhang, self.btn_nhaphang, self.btn_kiemkho, self.btn_khachhang, self.btn_nhanvien]
        for btn in self.buttons: 
            sidebar_layout.addWidget(btn)

        # Lệnh này đẩy tất cả các nút bên trên lên trên cùng
        sidebar_layout.addStretch()

        # THÊM NÚT ĐĂNG XUẤT VÀO ĐÂY (Nó sẽ nằm dưới cùng nhờ addStretch)
        sidebar_layout.addWidget(self.btn_logout)

        # ===== STACKED WIDGET =====
        self.stack = QStackedWidget()

        # KHỞI TẠO CÁC TRANG THẬT
        self.page_banhang = NvBanHangView()
        self.page_nhaphang = NvKhoView()
        self.page_khachhang = NvKhachHangView()
        self.ctrl_khachhang = NvKhachHangController(self.page_khachhang)

        self.page_kiemkho = self.create_temp_page("Trang Kiểm Kho & Báo Hủy")
        self.page_nhanvien = self.create_temp_page("Thông Tin Nhân Viên")

        # ADD VÀO STACK
        self.stack.addWidget(self.page_banhang)   # 0
        self.stack.addWidget(self.page_nhaphang)  # 1
        self.stack.addWidget(self.page_kiemkho)   # 2
        self.stack.addWidget(self.page_khachhang) # 3
        self.stack.addWidget(self.page_nhanvien)  # 4

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        # ===== KẾT NỐI SỰ KIỆN =====
        self.btn_banhang.clicked.connect(lambda: self.switch_page(self.page_banhang, self.btn_banhang))
        self.btn_nhaphang.clicked.connect(lambda: self.switch_page(self.page_nhaphang, self.btn_nhaphang))
        self.btn_kiemkho.clicked.connect(lambda: self.switch_page(self.page_kiemkho, self.btn_kiemkho))
        self.btn_khachhang.clicked.connect(lambda: self.switch_page(self.page_khachhang, self.btn_khachhang))
        self.btn_nhanvien.clicked.connect(lambda: self.switch_page(self.page_nhanvien, self.btn_nhanvien))

        # Kết nối sự kiện đăng xuất
        self.btn_logout.clicked.connect(self.handle_logout)

        # Mặc định mở trang bán hàng
        self.switch_page(self.page_banhang, self.btn_banhang)

    def create_nav_btn(self, text):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { 
                padding: 15px; 
                text-align: left; 
                border: none; 
                font-size: 14px; 
                background: transparent; 
                color: white; 
            }
            QPushButton:hover { background-color: #388e3c; } 
            QPushButton:checked { background-color: #1b5e20; font-weight: bold; }
        """)
        return btn

    def switch_page(self, page, button):
        self.stack.setCurrentWidget(page)
        # Bổ sung self.btn_logout vào danh sách reset nếu cần, 
        # nhưng thường nút Logout không cần giữ trạng thái Checked
        for b in self.buttons: 
            b.setChecked(False)
        button.setChecked(True)

    def create_temp_page(self, title):
        p = QWidget(); l = QVBoxLayout(p)
        lbl = QLabel(title); lbl.setStyleSheet("font-size: 22px; padding: 20px;")
        l.addWidget(lbl); l.addStretch(); return p
    
    def handle_logout(self):
        # Import tại đây để tránh lỗi Circular Import
        from views.login_view import LoginView
        from controllers.login_controller import LoginController
        
        self.login_window = LoginView()
        self.login_ctrl = LoginController(self.login_window)
        self.login_window.show()
        self.close()