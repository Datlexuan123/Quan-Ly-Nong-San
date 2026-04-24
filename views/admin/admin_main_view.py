# views/admin/admin_main_view.py

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt

# Import các trang nội dung
from views.admin.admin_nhanvien_view import AdminNhanVienView
from views.admin.admin_dashboard_view import AdminDashboardView
from views.admin.admin_ncc_view import AdminNCCView
from views.admin.admin_baocao_view import AdminBaoCaoView
from views.admin.admin_sanpham_view import AdminSanPhamView

class AdminMainView(QMainWindow):
    def __init__(self, user_data=None): # SỬA TẠI ĐÂY: Nhận user_data
        super().__init__()
        self.user_data = user_data if user_data else {} # Lưu lại thông tin
        
        self.setWindowTitle("HỆ THỐNG QUẢN TRỊ - NÔNG SẢN SẠCH")
        self.setGeometry(100, 100, 1400, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== SIDEBAR =====
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("background-color: #1b5e20; color: white;")
        sidebar_layout = QVBoxLayout(self.sidebar)

        # Hiển thị tên Admin đang đăng nhập
        ten_admin = self.user_data.get('ho_ten', 'Quản trị viên')
        self.lbl_welcome = QLabel(f"Xin chào,\n<b>{ten_admin}</b>")
        self.lbl_welcome.setStyleSheet("font-size: 16px; padding: 20px; color: #fff; border-bottom: 1px solid #2e7d32;")
        self.lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(self.lbl_welcome)

        # Menu buttons
        self.menu_buttons = []
        self.btn_dashboard = self.create_menu_btn("📊 Dashboard")
        self.btn_nhanvien = self.create_menu_btn("👥 Quản lý Nhân viên")
        self.btn_sanpham = self.create_menu_btn("🍎 Quản lý Sản phẩm")
        self.btn_ncc = self.create_menu_btn("🏭 Nhà cung cấp")
        self.btn_baocao = self.create_menu_btn("📈 Báo cáo Doanh thu")
        
        # Thêm các nút vào layout
        for btn in [self.btn_dashboard, self.btn_nhanvien, self.btn_sanpham, self.btn_ncc, self.btn_baocao]:
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        sidebar_layout.addStretch()

        self.btn_logout = QPushButton("🚪 Đăng xuất")
        self.btn_logout.setStyleSheet("padding: 15px; background: #d32f2f; color: white; border: none;")
        self.btn_logout.clicked.connect(self.handle_logout)
        sidebar_layout.addWidget(self.btn_logout)

        main_layout.addWidget(self.sidebar)

        # ===== CONTENT AREA (QStackedWidget) =====
        self.stack = QStackedWidget()
        
        # Khởi tạo các trang và truyền user_data vào nếu trang đó cần dùng
        self.page_dashboard = AdminDashboardView()
        self.page_nhanvien = AdminNhanVienView()
        self.page_sanpham = AdminSanPhamView()
        self.page_ncc = AdminNCCView()
        self.page_baocao = AdminBaoCaoView()

        self.stack.addWidget(self.page_dashboard) # Index 0
        self.stack.addWidget(self.page_nhanvien)  # Index 1
        self.stack.addWidget(self.page_sanpham)   # Index 2
        self.stack.addWidget(self.page_ncc)       # Index 3
        self.stack.addWidget(self.page_baocao)    # Index 4

        main_layout.addWidget(self.stack)

        # Kết nối sự kiện chuyển trang
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, self.btn_dashboard))
        self.btn_nhanvien.clicked.connect(lambda: self.switch_page(1, self.btn_nhanvien))
        self.btn_sanpham.clicked.connect(lambda: self.switch_page(2, self.btn_sanpham))
        self.btn_ncc.clicked.connect(lambda: self.switch_page(3, self.btn_ncc))
        self.btn_baocao.clicked.connect(lambda: self.switch_page(4, self.btn_baocao))
        
        self.switch_page(0, self.btn_dashboard)

    def create_menu_btn(self, text):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { padding: 15px 20px; text-align: left; border: none; font-size: 15px; color: white; background-color: transparent; }
            QPushButton:hover { background-color: #2e7d32; }
            QPushButton:checked { background-color: #4caf50; font-weight: bold; }
        """)
        return btn

    def switch_page(self, index, clicked_btn):
        self.stack.setCurrentIndex(index)
        for btn in self.menu_buttons:
            btn.setChecked(False)
        clicked_btn.setChecked(True)

    def handle_logout(self):
        from views.login_view import LoginView
        from controllers.login_controller import LoginController
        self.login_window = LoginView()
        self.login_controller = LoginController(self.login_window)
        self.login_window.show()
        self.close()