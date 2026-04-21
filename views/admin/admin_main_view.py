import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt

# Import các trang nội dung thật
from views.admin.admin_nhanvien_view import AdminNhanVienView
from views.admin.admin_dashboard_view import AdminDashboardView
from views.admin.admin_ncc_view import AdminNCCView
from views.admin.admin_baocao_view import AdminBaoCaoView
from views.admin.admin_sanpham_view import AdminSanPhamView # Trang Sản phẩm mới

class AdminMainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HỆ THỐNG QUẢN TRỊ - NÔNG SẢN SẠCH")
        self.setGeometry(100, 100, 1400, 900)

        # Widget chính
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== SIDEBAR (MENU BÊN TRÁI) =====
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("background-color: #1b5e20; color: white;") 
        sidebar_layout = QVBoxLayout(self.sidebar)

        # Tiêu đề Admin
        admin_label = QLabel("QUẢN TRỊ VIÊN")
        admin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        admin_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 30px 10px; color: #a5d6a7;")
        sidebar_layout.addWidget(admin_label)

        # Các nút Menu
        self.btn_dashboard = self.create_menu_btn("📊 Dashboard")
        self.btn_nhanvien = self.create_menu_btn("👥 Quản lý Nhân viên")
        self.btn_ncc = self.create_menu_btn("🚛 Nhà Cung Cấp")
        self.btn_sanpham = self.create_menu_btn("🍎 Quản lý Sản phẩm")
        self.btn_baocao = self.create_menu_btn("📈 Báo cáo Thống kê")
        self.btn_logout = self.create_menu_btn("🚪 Đăng xuất")

        self.menu_buttons = [
            self.btn_dashboard, self.btn_nhanvien, 
            self.btn_ncc, self.btn_sanpham, self.btn_baocao
        ]

        for btn in self.menu_buttons:
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(self.btn_logout)

        # ===== STACKED WIDGET (VÙNG NỘI DUNG) =====
        self.stack = QStackedWidget()
        
        # Khởi tạo các trang nội dung thật
        self.page_dashboard = AdminDashboardView()
        self.page_nhanvien = AdminNhanVienView()
        self.page_ncc = AdminNCCView()
        self.page_sanpham = AdminSanPhamView() # Đã thay bằng trang thật
        self.page_baocao = AdminBaoCaoView()

        # Thêm vào stack theo đúng thứ tự index
        self.stack.addWidget(self.page_dashboard) # index 0
        self.stack.addWidget(self.page_nhanvien)  # index 1
        self.stack.addWidget(self.page_ncc)       # index 2
        self.stack.addWidget(self.page_sanpham)   # index 3
        self.stack.addWidget(self.page_baocao)    # index 4

        # Thêm Sidebar và Stack vào Layout chính
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        # ===== KẾT NỐI SỰ KIỆN CHUYỂN TRANG =====
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, self.btn_dashboard))
        self.btn_nhanvien.clicked.connect(lambda: self.switch_page(1, self.btn_nhanvien))
        self.btn_ncc.clicked.connect(lambda: self.switch_page(2, self.btn_ncc))
        self.btn_sanpham.clicked.connect(lambda: self.switch_page(3, self.btn_sanpham))
        self.btn_baocao.clicked.connect(lambda: self.switch_page(4, self.btn_baocao))
        
        # Kết nối nút Đăng xuất
        self.btn_logout.clicked.connect(self.handle_logout)
        
        # Mặc định mở Dashboard
        self.switch_page(0, self.btn_dashboard)

    def create_menu_btn(self, text):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        style = """
            QPushButton {
                padding: 15px 20px;
                text-align: left;
                border: none;
                font-size: 15px;
                color: white;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #2e7d32;
            }
            QPushButton:checked {
                background-color: #4caf50;
                font-weight: bold;
            }
        """
        btn.setStyleSheet(style)
        return btn

    def switch_page(self, index, clicked_btn):
        self.stack.setCurrentIndex(index)
        for btn in self.menu_buttons:
            btn.setChecked(False)
        clicked_btn.setChecked(True)

    def handle_logout(self):
        # Import cục bộ để tránh lỗi vòng lặp
        from views.login_view import LoginView
        from controllers.login_controller import LoginController
        
        # Tạo lại cửa sổ và bộ điều khiển đăng nhập
        self.login_window = LoginView()
        self.login_ctrl = LoginController(self.login_window)
        
        self.login_window.show()
        self.close() # Đóng cửa sổ Admin hiện tại