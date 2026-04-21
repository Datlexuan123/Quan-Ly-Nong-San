from config.database import get_connection
from PyQt6.QtWidgets import QMessageBox
from views.nv.nv_main_view import NvMainView
# Thêm import trang Admin
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
            
            # --- CẬP NHẬT SQL: Kiểm tra thêm điều kiện trang_thai = 0 ---
            sql = "SELECT * FROM nhan_vien WHERE username = %s AND password = %s AND trang_thai = 0"
            cursor.execute(sql, (user_input, pwd_input))
            account = cursor.fetchone()

            if account:
                self.view.hide()
                # LOGIC PHÂN QUYỀN
                if account['chuc_vu'] == 'admin':
                    self.main_window = AdminMainView()
                    print(f"Đăng nhập thành công: Quyền Quản trị ({account['ho_ten']})")
                else:
                    self.main_window = NvMainView()
                    print(f"Đăng nhập thành công: Quyền Nhân viên ({account['ho_ten']})")
                
                self.main_window.show()
                conn.close()
            else:
                # KIỂM TRA LÝ DO THẤT BẠI: Do sai pass hay do bị khóa?
                sql_check = "SELECT trang_thai FROM nhan_vien WHERE username = %s AND password = %s"
                cursor.execute(sql_check, (user_input, pwd_input))
                check_lock = cursor.fetchone()
                conn.close()

                if check_lock and check_lock['trang_thai'] == 1:
                    QMessageBox.warning(self.view, "Tài khoản bị khóa", 
                                        f"Tài khoản '{user_input}' hiện đang bị khóa.\nVui lòng liên hệ Admin để mở lại.")
                else:
                    QMessageBox.warning(self.view, "Lỗi đăng nhập", "Sai tài khoản hoặc mật khẩu!")

        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi kết nối", f"Không thể kết nối cơ sở dữ liệu: {e}")