from config.database import get_connection
from PyQt6.QtWidgets import QMessageBox

class NvCaNhanController:
    def __init__(self, view):
        self.view = view
        self.view.btn_update_pwd.clicked.connect(self.change_password)

    def change_password(self):
        old_pwd = self.view.txt_old_pwd.text().strip()
        new_pwd = self.view.txt_new_pwd.text().strip()
        confirm_pwd = self.view.txt_confirm_pwd.text().strip()
        
        # Kiểm tra nếu user_info tồn tại
        if not self.view.user_info or 'id' not in self.view.user_info:
            QMessageBox.critical(self.view, "Lỗi", "Không tìm thấy thông tin nhân viên!")
            return
            
        user_id = self.view.user_info['id']

        if not old_pwd or not new_pwd:
            QMessageBox.warning(self.view, "Lỗi", "Vui lòng nhập đầy đủ mật khẩu!")
            return

        if new_pwd != confirm_pwd:
            QMessageBox.warning(self.view, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Sửa tên cột thành 'password' theo database của bạn
            cursor.execute("SELECT password FROM nhan_vien WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            if not user or user['password'] != old_pwd:
                QMessageBox.critical(self.view, "Lỗi", "Mật khẩu hiện tại không chính xác!")
                return

            # Cập nhật mật khẩu mới vào cột 'password'
            cursor.execute("UPDATE nhan_vien SET password = %s WHERE id = %s", (new_pwd, user_id))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self.view, "Thành công", "Đã cập nhật mật khẩu mới!")
            self.view.txt_old_pwd.clear()
            self.view.txt_new_pwd.clear()
            self.view.txt_confirm_pwd.clear()
            
        except Exception as e:
            QMessageBox.critical(self.view, "Lỗi", f"Lỗi hệ thống: {e}")