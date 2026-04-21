from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QHeaderView, QMessageBox, QFrame, QLineEdit, QComboBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from config.database import get_connection

class AdminSanPhamView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # --- THANH TIÊU ĐỀ (HEADER) ---
        header = QHBoxLayout()
        title = QLabel("QUẢN LÝ KHO HÀNG (ADMIN)")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1b5e20;")
        
        self.btn_add = QPushButton("+ Thêm Sản Phẩm")
        self.btn_add.setStyleSheet("""
            QPushButton { background-color: #2e7d32; color: white; padding: 8px 15px; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #388e3c; }
        """)
        
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.btn_add)
        layout.addLayout(header)

        # --- THANH TÌM KIẾM & BỘ LỌC ---
        filter_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Tìm tên hoặc mã sản phẩm...")
        self.txt_search.setFixedWidth(250)
        self.txt_search.textChanged.connect(self.load_data)

        self.btn_refresh = QPushButton("🔄 Làm mới")
        self.btn_refresh.clicked.connect(self.load_data)
        
        filter_layout.addWidget(self.txt_search)
        filter_layout.addStretch()
        filter_layout.addWidget(self.btn_refresh)
        layout.addLayout(filter_layout)

        # --- BẢNG DỮ LIỆU ---
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Sản Phẩm", "Giá & Tồn Kho", "ĐVT", "Trạng Thái", "Cập Nhật Nhanh", "Sửa", "Xóa"
        ])
        
        # Cấu hình độ rộng các cột
        header_view = self.table.horizontalHeader()
        self.table.setColumnWidth(0, 40)    # ID thu nhỏ tối đa
        self.table.setColumnWidth(1, 200)   # Tên sản phẩm thu gọn
        self.table.setColumnWidth(3, 60)    # Đơn vị tính
        self.table.setColumnWidth(5, 260)   # Bộ 3 nút trạng thái
        
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(100)
        
        layout.addWidget(self.table)

    def create_product_card(self, ten_sp, hinh_anh):
        """ Tạo thẻ sản phẩm gồm ảnh thu nhỏ và tên (Tiếng Việt) """
        card = QFrame()
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(5, 5, 5, 5)
        
        lbl_img = QLabel()
        lbl_img.setFixedSize(75, 75)
        path = f"assets/images/{hinh_anh if hinh_anh else 'no_image.png'}"
        pixmap = QPixmap(path)
        if pixmap.isNull():
            pixmap = QPixmap("assets/images/no_image.png")
            
        lbl_img.setPixmap(pixmap.scaled(75, 75, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        lbl_img.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        
        lbl_name = QLabel(ten_sp)
        lbl_name.setWordWrap(True)
        lbl_name.setStyleSheet("font-weight: bold; font-size: 13px; color: #2e3d49;")
        
        card_layout.addWidget(lbl_img)
        card_layout.addWidget(lbl_name)
        return card

    def create_status_buttons(self, p_id):
        """ Bộ 3 nút cập nhật trạng thái nhanh cho Admin """
        container = QWidget()
        l = QHBoxLayout(container)
        l.setContentsMargins(2, 2, 2, 2)
        l.setSpacing(5)

        btn_on = QPushButton("Còn hàng")
        btn_on.setStyleSheet("background-color: #4caf50; color: white; font-size: 10px; font-weight: bold; padding: 6px;")
        btn_on.clicked.connect(lambda: self.update_status(p_id, 0))

        btn_out = QPushButton("Hết hàng")
        btn_out.setStyleSheet("background-color: #ff9800; color: white; font-size: 10px; font-weight: bold; padding: 6px;")
        btn_out.clicked.connect(lambda: self.set_out_of_stock(p_id))

        btn_off = QPushButton("Ngừng bán")
        btn_off.setStyleSheet("background-color: #f44336; color: white; font-size: 10px; font-weight: bold; padding: 6px;")
        btn_off.clicked.connect(lambda: self.update_status(p_id, 1))

        l.addWidget(btn_on); l.addWidget(btn_out); l.addWidget(btn_off)
        return container

    def load_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            search_text = self.txt_search.text()
            
            query = """
                SELECT s.*, d.ten_dvt 
                FROM san_pham s 
                LEFT JOIN don_vi_tinh d ON s.id_dvt = d.id
                WHERE s.ten_sp LIKE %s OR s.id LIKE %s
            """
            cursor.execute(query, (f"%{search_text}%", f"%{search_text}%"))
            rows = cursor.fetchall()
            
            self.table.setRowCount(0)
            for r in rows:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                # 0. ID
                item_id = QTableWidgetItem(str(r['id']))
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 0, item_id)
                
                # 1. Thẻ Sản Phẩm (Ảnh + Tên)
                self.table.setCellWidget(row, 1, self.create_product_card(r['ten_sp'], r['hinh_anh']))
                
                # 2. Giá & Kho
                gia = float(r['gia_ban'])
                ton = r['so_luong_ton']
                self.table.setItem(row, 2, QTableWidgetItem(f"Giá: {gia:,.0f} đ\nKho: {ton}"))
                
                # 3. ĐVT
                self.table.setItem(row, 3, QTableWidgetItem(str(r['ten_dvt'])))
                
                # 4. Trạng Thái Hiện Tại
                st_text = "🟢 Còn hàng" if r['trang_thai'] == 0 else "🔴 Ngừng bán"
                if r['so_luong_ton'] <= 0 and r['trang_thai'] == 0:
                    st_text = "🟠 Hết hàng"
                self.table.setItem(row, 4, QTableWidgetItem(st_text))

                # 5. Bộ nút cập nhật nhanh
                self.table.setCellWidget(row, 5, self.create_status_buttons(r['id']))
                
                # 6. Nút Sửa
                btn_edit = QPushButton("Sửa")
                btn_edit.setStyleSheet("background-color: #2196f3; color: white; font-weight: bold;")
                self.table.setCellWidget(row, 6, btn_edit)

                # 7. Nút Xóa (Ràng buộc: Không được xóa nếu còn hàng)
                btn_del = QPushButton("Xóa")
                if ton > 0:
                    btn_del.setEnabled(False)
                    btn_del.setStyleSheet("background-color: #e0e0e0; color: #9e9e9e; border: 1px solid #bdbdbd;")
                    btn_del.setToolTip("Cần cập nhật 'Hết hàng' trước khi xóa!")
                else:
                    btn_del.setStyleSheet("background-color: #333333; color: white; font-weight: bold;")
                    btn_del.clicked.connect(lambda _, pid=r['id']: self.delete_product(pid))
                self.table.setCellWidget(row, 7, btn_del)

            conn.close()
        except Exception as e:
            print(f"Lỗi load dữ liệu: {e}")

    def update_status(self, p_id, status):
        try:
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("UPDATE san_pham SET trang_thai = %s WHERE id = %s", (status, p_id))
            conn.commit(); conn.close(); self.load_data()
        except Exception as e: QMessageBox.critical(self, "Lỗi", str(e))

    def set_out_of_stock(self, p_id):
        try:
            conn = get_connection(); cursor = conn.cursor()
            cursor.execute("UPDATE san_pham SET so_luong_ton = 0 WHERE id = %s", (p_id,))
            conn.commit(); conn.close(); self.load_data()
        except Exception as e: QMessageBox.critical(self, "Lỗi", str(e))

    def delete_product(self, p_id):
        confirm = QMessageBox.question(self, "Xác nhận xóa", 
                                      f"Bạn có chắc chắn muốn xóa vĩnh viễn sản phẩm ID {p_id}?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                conn = get_connection(); cursor = conn.cursor()
                cursor.execute("DELETE FROM san_pham WHERE id = %s", (p_id,))
                conn.commit(); conn.close(); self.load_data()
            except Exception as e: QMessageBox.critical(self, "Lỗi", str(e))