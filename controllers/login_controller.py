# controllers/login_controller.py

from config.database import get_connection
from PyQt6.QtWidgets import QMessageBox
from views.nv.nv_main_view import NvMainView
from views.admin.admin_main_view import AdminMainView

class LoginController:
    def __init__(self, view):
        self.view = view
        self.view.btn_login.clicked.connect(self.handle_login)

    def handle_login(self):
        user_input = self.view.txt_username.text()
        pwd_input = self.view.txt_password.text()

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Kiểm tra tài khoản hoạt động
            sql = "SELECT * FROM nhan_vien WHERE username = %s AND password = %s AND trang_thai = 0"
            cursor.execute(sql, (user_input, pwd_input))
            account = cursor.fetchone()

            if account:
                self.view.hide()
                # TRUYỀN BIẾN account vào cả hai giao diện
                if account['chuc_vu'] == 'admin':
                    self.main_window = AdminMainView(account) # Đã thêm tham số
                    print(f"Đăng nhập Admin: {account['ho_ten']}")
                else:
                    self.main_window = NvMainView(account)
                    print(f"Đăng nhập Nhân viên: {account['ho_ten']}")
                
                self.main_window.show()
                conn.close()
            else:
                # Kiểm tra tài khoản bị khóa
                sql_check = "SELECT trang_thai FROM nhan_vien WHERE username = %s AND password = %s"
                cursor.execute(sql_check, (user_input, pwd_input))
                check_lock = cursor.fetchone()
                conn.close()

                if check_lock and check_lock['trang_thai'] == 1:
                    QMessageBox.warning(self.view, "Tài khoản bị khóa", "Tài khoản này hiện đang bị khóa.")
                else:
                    QMessageBox.warning(self.view, "Lỗi đăng nhập", "Sai tài khoản hoặc mật khẩu!")

        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi", f"Lỗi kết nối: {e}")