import sys
from PyQt6.QtWidgets import QApplication
from views.login_view import LoginView
from controllers.login_controller import LoginController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Khởi tạo trang Login
    login_window = LoginView()
    # Kết nối logic cho trang Login
    login_ctrl = LoginController(login_window)
    
    login_window.show()
    sys.exit(app.exec())