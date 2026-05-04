# views/admin/admin_main_view.py

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt

# ===== IMPORT CÁC TRANG NỘI BỘ ADMIN =====
from views.admin.admin_nhanvien_view import AdminNhanVienView
from views.admin.admin_dashboard_view import AdminDashboardView
from views.admin.admin_ncc_view import AdminNCCView
from views.admin.admin_baocao_view import AdminBaoCaoView
from views.admin.admin_sanpham_view import AdminSanPhamView
from views.admin.admin_log_view import AdminLogView
from views.admin.admin_duyet_huy_view import AdminDuyetHuyView # THÊM DÒNG NÀY

# ===== IMPORT TRANG KHO (Tái sử dụng từ phía NV) =====
from views.nv.nv_kho_history_view import NvKhoHistoryView
from controllers.nv_kho_history_controller import NvKhoHistoryController

# ===== IMPORT CONTROLLER QUẢN LÝ SẢN PHẨM & DUYỆT HỦY =====
from controllers.admin_sanpham_controller import AdminSanPhamController
from controllers.admin_duyet_huy_controller import AdminDuyetHuyController # THÊM DÒNG NÀY
from models.kiemkho_model import KiemKhoModel # THÊM DÒNG NÀY

class AdminMainView(QMainWindow):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data if user_data else {}
        
        self.setWindowTitle("HỆ THỐNG QUẢN TRỊ - NÔNG SẢN SẠCH")
        self.setGeometry(100, 100, 1400, 900)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== SIDEBAR (Thanh điều hướng bên trái) =====
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("background-color: #1b5e20; color: white;")
        sidebar_layout = QVBoxLayout(self.sidebar)

        # Thông tin Admin đăng nhập
        ten_admin = self.user_data.get('ho_ten', 'Quản trị viên')
        self.lbl_welcome = QLabel(f"Xin chào,\n<b>{ten_admin}</b>")
        self.lbl_welcome.setStyleSheet("font-size: 16px; padding: 20px; color: #fff; border-bottom: 1px solid #2e7d32;")
        self.lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(self.lbl_welcome)

        # Danh sách nút Menu
        self.menu_buttons = []
        self.btn_dashboard = self.create_menu_btn("📊 Dashboard")
        self.btn_nhanvien = self.create_menu_btn("👥 Quản lý Nhân viên")
        self.btn_sanpham = self.create_menu_btn("🍎 Quản lý Sản phẩm")
        self.btn_kho = self.create_menu_btn("📦 Lịch sử nhập kho") 
        self.btn_duyet_huy = self.create_menu_btn("🔔 Phê duyệt báo hủy") # THÊM NÚT NÀY
        self.btn_ncc = self.create_menu_btn("🏭 Nhà cung cấp")
        self.btn_baocao = self.create_menu_btn("📈 Báo cáo Doanh thu")
        self.btn_log = self.create_menu_btn("🛡️ Nhật ký hoạt động")
        
        # Cập nhật danh sách menu list
        self.menu_list = [
            self.btn_dashboard, self.btn_nhanvien, self.btn_sanpham, 
            self.btn_kho, self.btn_duyet_huy, self.btn_ncc, self.btn_baocao, self.btn_log
        ]
        
        for btn in self.menu_list:
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        sidebar_layout.addStretch()

        # Nút Đăng xuất
        self.btn_logout = QPushButton("🚪 Đăng xuất")
        self.btn_logout.setStyleSheet("padding: 15px; background: #d32f2f; color: white; border: none; font-weight: bold;")
        self.btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_logout.clicked.connect(self.handle_logout)
        sidebar_layout.addWidget(self.btn_logout)

        main_layout.addWidget(self.sidebar)

        # ===== CONTENT AREA (QStackedWidget) =====
        self.stack = QStackedWidget()
        
        # 1. Khởi tạo các trang nội dung
        self.page_dashboard = AdminDashboardView()
        self.page_nhanvien = AdminNhanVienView()
        self.page_sanpham = AdminSanPhamView()
        self.page_kho = NvKhoHistoryView() 
        self.page_duyet_huy = AdminDuyetHuyView() # TRANG MỚI
        self.page_ncc = AdminNCCView()
        self.page_baocao = AdminBaoCaoView()
        self.page_log = AdminLogView()

        # 2. Khởi tạo các Controller
        self.ctrl_kho = NvKhoHistoryController(self.page_kho)
        self.ctrl_sanpham = AdminSanPhamController(self.page_sanpham, self.user_data)
        self.model_kiemkho = KiemKhoModel() # Dùng chung model
        self.ctrl_duyet_huy = AdminDuyetHuyController(self.page_duyet_huy, self.model_kiemkho) # CONTROLLER MỚI

        # 3. Thêm vào stack (Lưu ý thứ tự index thay đổi)
        self.stack.addWidget(self.page_dashboard)  # 0
        self.stack.addWidget(self.page_nhanvien)   # 1
        self.stack.addWidget(self.page_sanpham)    # 2
        self.stack.addWidget(self.page_kho)        # 3
        self.stack.addWidget(self.page_duyet_huy)  # 4 (VỊ TRÍ MỚI)
        self.stack.addWidget(self.page_ncc)        # 5
        self.stack.addWidget(self.page_baocao)     # 6
        self.stack.addWidget(self.page_log)        # 7

        main_layout.addWidget(self.stack)

        # 4. Kết nối sự kiện chuyển trang
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0, self.btn_dashboard))
        self.btn_nhanvien.clicked.connect(lambda: self.switch_page(1, self.btn_nhanvien))
        self.btn_sanpham.clicked.connect(lambda: self.switch_page(2, self.btn_sanpham))
        self.btn_kho.clicked.connect(lambda: self.switch_page(3, self.btn_kho))
        self.btn_duyet_huy.clicked.connect(lambda: self.switch_page(4, self.btn_duyet_huy)) # CONNECT NÚT MỚI
        self.btn_ncc.clicked.connect(lambda: self.switch_page(5, self.btn_ncc))
        self.btn_baocao.clicked.connect(lambda: self.switch_page(6, self.btn_baocao))
        self.btn_log.clicked.connect(lambda: self.switch_page(7, self.btn_log))
        
        # Mặc định mở Dashboard khi khởi chạy
        self.switch_page(0, self.btn_dashboard)

    def create_menu_btn(self, text):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton { padding: 15px 20px; text-align: left; border: none; font-size: 15px; color: white; background-color: transparent; }
            QPushButton:hover { background-color: #2e7d32; }
            QPushButton:checked { background-color: #4caf50; font-weight: bold; border-left: 5px solid #aed581; }
        """)
        return btn

    def switch_page(self, index, clicked_btn):
        """Hàm chuyển trang và tự động làm mới dữ liệu"""
        self.stack.setCurrentIndex(index)
        
        if index == 0: self.page_dashboard.load_real_data()
        if index == 2: self.ctrl_sanpham.load_data()
        if index == 3: self.ctrl_kho.load_history()
        if index == 4: self.ctrl_duyet_huy.load_data() # LOAD DỮ LIỆU CHỜ DUYỆT
        if index == 7: self.page_log.load_data()

        # Cập nhật trạng thái hiển thị của các nút menu
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