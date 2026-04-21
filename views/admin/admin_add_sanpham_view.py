from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QComboBox
)
from config.database import get_connection

class AdminAddSanPhamView(QDialog):
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setWindowTitle("Thêm/Sửa Sản Phẩm")
        self.setFixedSize(400, 500)
        self.init_ui()
        
        if self.product_data:
            self.fill_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.txt_ten = QLineEdit(); self.txt_ten.setPlaceholderText("Tên sản phẩm")
        self.txt_gia = QLineEdit(); self.txt_gia.setPlaceholderText("Giá bán")
        self.txt_ton = QLineEdit(); self.txt_ton.setPlaceholderText("Số lượng tồn")
        
        # ComboBox đơn vị tính (DVT)
        self.cbo_dvt = QComboBox()
        self.load_dvt()

        layout.addWidget(QLabel("Tên sản phẩm:"))
        layout.addWidget(self.txt_ten)
        layout.addWidget(QLabel("Giá bán:"))
        layout.addWidget(self.txt_gia)
        layout.addWidget(QLabel("Số lượng tồn:"))
        layout.addWidget(self.txt_ton)
        layout.addWidget(QLabel("Đơn vị tính:"))
        layout.addWidget(self.cbo_dvt)

        self.btn_save = QPushButton("LƯU THÔNG TIN")
        self.btn_save.setStyleSheet("background-color: #2e7d32; color: white; padding: 10px; font-weight: bold;")
        self.btn_save.clicked.connect(self.save_data)
        layout.addWidget(self.btn_save)

    def load_dvt(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM don_vi_tinh")
        for d in cursor.fetchall():
            self.cbo_dvt.addItem(d['ten_dvt'], d['id'])
        conn.close()

    def fill_data(self):
        self.txt_ten.setText(self.product_data['ten_sp'])
        self.txt_gia.setText(str(self.product_data['gia_ban']))
        self.txt_ton.setText(str(self.product_data['so_luong_ton']))
        # Tìm index của DVT
        idx = self.cbo_dvt.findData(self.product_data['id_dvt'])
        self.cbo_dvt.setCurrentIndex(idx)

    def save_data(self):
        ten = self.txt_ten.text()
        gia = self.txt_gia.text()
        ton = self.txt_ton.text()
        id_dvt = self.cbo_dvt.currentData()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            if self.product_data: # UPDATE
                sql = "UPDATE san_pham SET ten_sp=%s, gia_ban=%s, so_luong_ton=%s, id_dvt=%s WHERE id=%s"
                cursor.execute(sql, (ten, gia, ton, id_dvt, self.product_data['id']))
            else: # INSERT
                sql = "INSERT INTO san_pham (ten_sp, gia_ban, so_luong_ton, id_dvt, trang_thai) VALUES (%s, %s, %s, %s, 0)"
                cursor.execute(sql, (ten, gia, ton, id_dvt))
            
            conn.commit()
            conn.close()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))