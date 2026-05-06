import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox
from views.login_view import LoginView
from controllers.login_controller import LoginController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        # Khởi tạo trang Login
        login_window = LoginView()
        login_ctrl = LoginController(login_window)
        login_window.show()
        
        # Chạy ứng dụng
        sys.exit(app.exec())
    except Exception as e:
        # Nếu có lỗi, nó sẽ hiện một hộp thoại báo lỗi ngay trên màn hình
        error_msg = traceback.format_exc()
        print(f"--- LỖI HỆ THỐNG ---\n{error_msg}")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Ứng dụng bị sập!")
        msg.setInformativeText(error_msg)
        msg.setWindowTitle("Lỗi")
        msg.exec()