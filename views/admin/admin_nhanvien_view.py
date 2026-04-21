from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QHeaderView, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from config.database import get_connection
# Đảm bảo bạn đã có file này trong thư mục views/admin/
from views.admin.admin_add_nhanvien_view import AdminAddNhanVienView

class AdminNhanVienView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data() # Gọi hàm nạp dữ liệu ngay khi khởi tạo

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # ---------- HEADER & NÚT THÊM ----------
        header_layout = QHBoxLayout()
        title = QLabel("QUẢN LÝ NHÂN VIÊN")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1b5e20;")
        
        self.btn_add_form = QPushButton("+ Nhân viên")
        self.btn_add_form.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_form.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32; color: white; padding: 10px 20px; 
                font-weight: bold; border-radius: 5px;
            }
            QPushButton:hover { background-color: #388e3c; }
        """)
        
        # KẾT NỐI SỰ KIỆN MỞ FORM THÊM NHÂN VIÊN
        self.btn_add_form.clicked.connect(self.open_add_form)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_add_form)
        self.main_layout.addLayout(header_layout)

        # ---------- BẢNG DỮ LIỆU ----------
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Mã NV", "Họ Tên", "Tài Khoản", "Chức Vụ", "Trạng Thái", "Thao Tác"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("QTableWidget { background-color: white; font-size: 14px; }")
        
        self.main_layout.addWidget(self.table)

    def load_data(self):
        """Kết nối Database và lấy dữ liệu từ bảng nhan_vien"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT ma_nv, ho_ten, username, chuc_vu, trang_thai FROM nhan_vien")
            rows = cursor.fetchall()
            
            self.table.setRowCount(0)
            for row_data in rows:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                self.table.setItem(row, 0, QTableWidgetItem(str(row_data['ma_nv'])))
                self.table.setItem(row, 1, QTableWidgetItem(str(row_data['ho_ten'])))
                self.table.setItem(row, 2, QTableWidgetItem(str(row_data['username'])))
                self.table.setItem(row, 3, QTableWidgetItem(str(row_data['chuc_vu'])))
                
                is_locked = row_data['trang_thai'] == 1
                status = "Đã khóa" if is_locked else "Đang hoạt động"
                status_item = QTableWidgetItem(status)
                
                if is_locked:
                    status_item.setForeground(Qt.GlobalColor.red)
                else:
                    status_item.setForeground(Qt.GlobalColor.darkGreen)
                
                self.table.setItem(row, 4, status_item)

                # Cột thao tác
                btn_container = QWidget()
                btn_layout = QHBoxLayout(btn_container)
                btn_layout.setContentsMargins(5, 2, 5, 2)
                btn_layout.setSpacing(5)

                btn_lock = QPushButton("Mở" if is_locked else "Khóa")
                btn_lock.setFixedWidth(60)
                color = "#4caf50" if is_locked else "#f44336" 
                btn_lock.setStyleSheet(f"background-color: {color}; color: white; border-radius: 3px; font-weight: bold;")
                btn_lock.clicked.connect(lambda checked, u=row_data['username'], s=row_data['trang_thai']: self.handle_lock(u, s))
                
                btn_reset = QPushButton("MK")
                btn_reset.setFixedWidth(45)
                btn_reset.setStyleSheet("background-color: #2196f3; color: white; border-radius: 3px; font-weight: bold;")
                btn_reset.clicked.connect(lambda checked, u=row_data['username']: self.handle_reset_password(u))

                btn_layout.addWidget(btn_lock)
                btn_layout.addWidget(btn_reset)
                self.table.setCellWidget(row, 5, btn_container)
                
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Database", f"Không thể lấy dữ liệu: {e}")

    def open_add_form(self):
        """Mở cửa sổ QDialog để thêm nhân viên mới"""
        # Thay vì import ở đầu file, ta có thể import trực tiếp tại đây nếu vẫn lỗi
        from views.admin.admin_add_nhanvien_view import AdminAddNhanVienView 
        
        self.add_diag = AdminAddNhanVienView(self)
        if self.add_diag.exec():
            self.load_data()

    def handle_lock(self, username, current_status):
        new_status = 1 if current_status == 0 else 0
        action_text = "KHÓA" if current_status == 0 else "MỞ KHÓA"
        
        reply = QMessageBox.question(self, 'Xác nhận', f"Bạn có chắc chắn muốn {action_text} tài khoản {username}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE nhan_vien SET trang_thai = %s WHERE username = %s", (new_status, username))
                conn.commit()
                conn.close()
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Cập nhật thất bại: {e}")

    def handle_reset_password(self, username):
        reply = QMessageBox.question(self, 'Xác nhận', f"Đặt lại mật khẩu cho {username} về mặc định '123456'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE nhan_vien SET password = %s WHERE username = %s", ('123456', username))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Thành công", f"Đã đặt lại mật khẩu cho {username} thành '123456'")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể đặt lại mật khẩu: {e}")