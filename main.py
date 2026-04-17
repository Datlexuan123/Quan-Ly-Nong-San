import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
# Import class UI từ file bạn vừa convert ở Bước 1
from main_window import Ui_MainWindow 

class NongSanApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 1. Cấu hình bảng dữ liệu mẫu
        self.setup_table_data()
        
        # 2. Kết nối sự kiện cho các nút bấm
        self.ui.btn_add_new.clicked.connect(self.on_add_click)

    def setup_table_data(self):
        # Dữ liệu mẫu
        data = [
            ("P001", "Táo Envy", "Trái cây", "kg", "85,000đ", "50.5"),
            ("P002", "Bắp cải xanh", "Rau củ", "bó", "22,000đ", "120"),
            ("P003", "Cam Sành", "Trái cây", "kg", "40,000đ", "80.0"),
            ("P004", "Tỏi Lý Sơn", "Gia vị", "túi", "150,000đ", "15"),
        ]

        self.ui.table_data.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            # Điền ID
            self.ui.table_data.setItem(row_idx, 0, QTableWidgetItem(row_data[0]))
            # Cột 1 để trống cho hình ảnh (xử lý sau)
            self.ui.table_data.setItem(row_idx, 1, QTableWidgetItem("🖼️")) 
            # Điền các thông tin khác
            self.ui.table_data.setItem(row_idx, 2, QTableWidgetItem(row_data[1]))
            self.ui.table_data.setItem(row_idx, 3, QTableWidgetItem(row_data[2]))
            self.ui.table_data.setItem(row_idx, 4, QTableWidgetItem(row_data[3]))
            self.ui.table_data.setItem(row_idx, 5, QTableWidgetItem(row_data[4]))
            self.ui.table_data.setItem(row_idx, 6, QTableWidgetItem(row_data[5]))

            # Thêm nút Hành động (Sửa/Xóa) vào cột cuối
            self.add_action_buttons(row_idx)

    def add_action_buttons(self, row):
        # Tạo Widget chứa 2 nút bấm
        action_widget = QWidget()
        layout = QHBoxLayout(action_widget)
        btn_edit = QPushButton("📝")
        btn_delete = QPushButton("🗑️")
        
        # Style nhẹ cho nút trong bảng
        btn_edit.setFixedWidth(30)
        btn_delete.setFixedWidth(30)
        
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.ui.table_data.setCellWidget(row, 7, action_widget)

    def on_add_click(self):
        print("Mở form thêm sản phẩm mới...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NongSanApp()
    window.show()
    sys.exit(app.exec())