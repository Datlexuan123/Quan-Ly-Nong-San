from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt
from config.database import get_connection

class AdminNCCView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("QUẢN LÝ NHÀ CUNG CẤP")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1b5e20;")
        
        self.btn_add = QPushButton("+ Nhà cung cấp")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32; color: white; padding: 10px 20px; 
                font-weight: bold; border-radius: 5px;
            }
            QPushButton:hover { background-color: #388e3c; }
        """)
        self.btn_add.clicked.connect(self.open_add_form)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_add)
        self.main_layout.addLayout(header_layout)

        # Bảng dữ liệu - Khớp với các cột trong ảnh database của bạn
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tên Nhà Cung Cấp", "Số Điện Thoại", "Địa Chỉ", "Ghi Chú"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("QTableWidget { background-color: white; font-size: 14px; }")
        
        self.main_layout.addWidget(self.table)

    def load_data(self):
        """Lấy dữ liệu thật từ bảng nha_cung_cap"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # Truy vấn đúng các tên cột trong ảnh bạn gửi
            cursor.execute("SELECT id, ten_ncc, so_dien_thoai, dia_chi, ghi_chu FROM nha_cung_cap")
            rows = cursor.fetchall()
            
            self.table.setRowCount(0)
            for row_data in rows:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(row_data['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(str(row_data['ten_ncc'])))
                self.table.setItem(row, 2, QTableWidgetItem(str(row_data['so_dien_thoai'])))
                self.table.setItem(row, 3, QTableWidgetItem(str(row_data['dia_chi'])))
                self.table.setItem(row, 4, QTableWidgetItem(str(row_data['ghi_chu'])))
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi nạp dữ liệu", f"Lỗi: {str(e)}")

    def open_add_form(self):
        from views.admin.admin_add_ncc_view import AdminAddNCCView
        dialog = AdminAddNCCView(self)
        if dialog.exec():
            self.load_data()