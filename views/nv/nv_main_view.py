import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QTabWidget
)
from PyQt6.QtCore import Qt

# ===== IMPORT VIEW =====
from views.nv.nv_banhang_view import NvBanHangView
from views.nv.nv_kho_view import NvKhoView
from views.nv.nv_kho_history_view import NvKhoHistoryView # Cần import này
from views.nv.nv_khach_hang_view import NvKhachHangView 
from views.nv.nv_ca_nhan_view import NvCaNhanView
from views.nv.nv_don_hang_view import NvDonHangView

# ===== IMPORT CONTROLLER =====
from controllers.nv_khach_hang_controller import NvKhachHangController
from controllers.nv_ca_nhan_controller import NvCaNhanController
from controllers.nv_don_hang_controller import NvDonHangController
from controllers.nv_kho_history_controller import NvKhoHistoryController # Cần import này

class NvMainView(QMainWindow):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data 

        self.setWindowTitle("Giao diện nhân viên - Nông Sản Sạch")
        self.setGeometry(200, 200, 1300, 900)

        # ===== Widget chính =====
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== Sidebar =====
        sidebar = QFrame()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet("background-color: #2e7d32; color: white;")
        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("Nông Sản Sạch")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 25px 10px; border-bottom: 1px solid #4caf50;")
        sidebar_layout.addWidget(title)

        self.btn_banhang = self.create_nav_btn("🛒 Bán hàng")
        self.btn_donhang = self.create_nav_btn("📑 Đơn hàng ship")
        self.btn_nhaphang = self.create_nav_btn("📦 Kho & Nhập hàng")
        self.btn_kiemkho = self.create_nav_btn("📊 Kiểm kho & báo hủy")
        self.btn_khachhang = self.create_nav_btn("👥 Khách hàng")
        self.btn_nhanvien = self.create_nav_btn("👤 Thông tin NV")
        self.btn_logout = self.create_nav_btn("🚪 Đăng xuất")

        self.buttons = [
            self.btn_banhang, self.btn_donhang, self.btn_nhaphang, 
            self.btn_kiemkho, self.btn_khachhang, self.btn_nhanvien
        ]
        
        for btn in self.buttons: 
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_logout)

        # ===== STACKED WIDGET =====
        self.stack = QStackedWidget()

        # 1. Trang Bán hàng
        self.page_banhang = NvBanHangView()
        
        # 2. Trang Kho (SỬ DỤNG QTabWidget)
        self.container_kho = QWidget()
        layout_kho = QVBoxLayout(self.container_kho)
        layout_kho.setContentsMargins(0,0,0,0)
        
        self.tabs_kho = QTabWidget() # ĐỊNH NGHĨA BIẾN NÀY ĐỂ HẾT LỖI
        self.page_nhaphang = NvKhoView(self.user_data)
        self.page_kho_history = NvKhoHistoryView()
        
        self.tabs_kho.addTab(self.page_nhaphang, "📦 Nhập hàng mới")
        self.tabs_kho.addTab(self.page_kho_history, "📜 Lịch sử nhập kho")
        layout_kho.addWidget(self.tabs_kho)

        # 3. Các trang khác
        self.page_kiemkho = self.create_temp_page("Trang Kiểm Kho & Báo Hủy")
        self.page_khachhang = NvKhachHangView()
        self.page_nhanvien = NvCaNhanView(self.user_data)
        self.page_donhang = NvDonHangView()

        # ===== KHỞI TẠO CONTROLLER =====
        self.ctrl_khachhang = NvKhachHangController(self.page_khachhang)
        self.ctrl_nhanvien = NvCaNhanController(self.page_nhanvien)
        self.ctrl_donhang = NvDonHangController(self.page_donhang, self.user_data)
        self.ctrl_kho_history = NvKhoHistoryController(self.page_kho_history)

        # ADD VÀO STACK
        self.stack.addWidget(self.page_banhang)   # 0
        self.stack.addWidget(self.container_kho)  # 1 (Chứa cả Nhập hàng và Lịch sử)
        self.stack.addWidget(self.page_kiemkho)   # 2
        self.stack.addWidget(self.page_khachhang) # 3
        self.stack.addWidget(self.page_nhanvien)  # 4
        self.stack.addWidget(self.page_donhang)   # 5

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        # ===== KẾT NỐI SỰ KIỆN =====
        self.btn_banhang.clicked.connect(lambda: self.switch_page(self.page_banhang, self.btn_banhang))
        self.btn_donhang.clicked.connect(lambda: self.switch_page(self.page_donhang, self.btn_donhang))
        self.btn_nhaphang.clicked.connect(lambda: self.switch_page(self.container_kho, self.btn_nhaphang))
        self.btn_kiemkho.clicked.connect(lambda: self.switch_page(self.page_kiemkho, self.btn_kiemkho))
        self.btn_khachhang.clicked.connect(lambda: self.switch_page(self.page_khachhang, self.btn_khachhang))
        self.btn_nhanvien.clicked.connect(lambda: self.switch_page(self.page_nhanvien, self.btn_nhanvien))
        self.btn_logout.clicked.connect(self.handle_logout)
        
        # Sự kiện khi chuyển Tab trong Kho để tự động load lại dữ liệu lịch sử mới
        self.tabs_kho.currentChanged.connect(self.on_kho_tab_changed)

        self.switch_page(self.page_banhang, self.btn_banhang)

    def on_kho_tab_changed(self, index):
        if index == 1: # Tab Lịch sử
            self.ctrl_kho_history.load_history()

    def create_nav_btn(self, text):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { padding: 15px; text-align: left; border: none; font-size: 14px; background: transparent; color: white; }
            QPushButton:hover { background-color: #388e3c; } 
            QPushButton:checked { background-color: #1b5e20; font-weight: bold; border-left: 4px solid #aed581; }
        """)
        return btn

    def switch_page(self, page, button):
        self.stack.setCurrentWidget(page)
        for b in self.buttons: b.setChecked(False)
        button.setChecked(True)

    def create_temp_page(self, title):
        p = QWidget(); l = QVBoxLayout(p)
        lbl = QLabel(title); lbl.setStyleSheet("font-size: 20px; padding: 20px; color: #666;")
        l.addWidget(lbl); l.addStretch(); return p
    
    def handle_logout(self):
        from views.login_view import LoginView
        from controllers.login_controller import LoginController
        self.login_window = LoginView()
        self.login_ctrl = LoginController(self.login_window)
        self.login_window.show()
        self.close()