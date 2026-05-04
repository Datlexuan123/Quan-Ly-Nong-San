from PyQt6.QtWidgets import QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import Qt
from models.sanpham_model import SanPhamModel

class AdminSanPhamController:
    def __init__(self, view, user_data=None):
        self.view = view
        self.user_data = user_data if user_data else {}
        self.model = SanPhamModel()
        
        self.view.txt_search.textChanged.connect(self.load_data)
        self.view.btn_add.clicked.connect(self.handle_add)
        self.load_data()

    def load_data(self):
        """Tải dữ liệu và hiển thị trạng thái kinh doanh"""
        try:
            products = self.model.get_all()
            search_text = self.view.txt_search.text().lower()
            
            self.view.table.setRowCount(0)
            row = 0
            for p in products:
                ten = p.get('ten_sp', '').lower()
                nguon = (p.get('nguon_goc') or "").lower()
                
                if search_text in ten or search_text in nguon:
                    self.view.table.insertRow(row)
                    self.view.table.setItem(row, 0, QTableWidgetItem(str(p['id'])))
                    self.view.table.setItem(row, 1, QTableWidgetItem(p['ten_sp']))
                    self.view.table.setItem(row, 2, QTableWidgetItem(p.get('nguon_goc') or "Chưa rõ"))
                    
                    gia = float(p.get('gia_ban', 0))
                    self.view.table.setItem(row, 3, QTableWidgetItem(f"{gia:,.0f} đ"))
                    
                    ton = p.get('so_luong_ton', 0)
                    item_ton = QTableWidgetItem(str(ton))
                    if ton < 20: 
                        item_ton.setForeground(Qt.GlobalColor.red)
                    self.view.table.setItem(row, 4, item_ton)
                    
                    self.view.table.setItem(row, 5, QTableWidgetItem(str(p.get('han_su_dung', 'N/A'))))
                    self.add_action_buttons(row, p)
                    row += 1
        except Exception as e:
            print(f"Lỗi load sản phẩm: {e}")

    def add_action_buttons(self, row, p):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)

        # Nút Sửa
        btn_edit = QPushButton("Sửa")
        btn_edit.setFixedWidth(50)
        btn_edit.setStyleSheet("background-color: #1976d2; color: white; font-weight: bold; border-radius: 3px;")
        btn_edit.clicked.connect(lambda: QMessageBox.information(self.view, "Sửa", f"Sửa {p['ten_sp']}"))

        # Nút Trạng thái: 0 = Đang bán (Xanh), 1 = Dừng bán (Đỏ)[cite: 14]
        is_stopped = p.get('trang_thai', 0) == 1 
        
        btn_status = QPushButton("Đang bán" if not is_stopped else "Dừng bán")
        btn_status.setFixedWidth(80)
        
        # Thiết lập màu sắc dựa trên trạng thái[cite: 14]
        if not is_stopped:
            btn_status.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold; border-radius: 3px;")
        else:
            btn_status.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; border-radius: 3px;")

        btn_status.clicked.connect(lambda: self.toggle_product_status(p))

        layout.addWidget(btn_edit)
        layout.addWidget(btn_status)
        self.view.table.setCellWidget(row, 6, container)

    def toggle_product_status(self, p):
        """Đảo ngược trạng thái kinh doanh của sản phẩm và cập nhật DB[cite: 14, 15]"""
        current_status = p.get('trang_thai', 0)
        new_status = 1 if current_status == 0 else 0
        status_text = "DỪNG BÁN" if new_status == 1 else "TIẾP TỤC BÁN"
        
        reply = QMessageBox.question(self.view, "Xác nhận", 
                                     f"Bạn có chắc muốn {status_text} mặt hàng {p['ten_sp']}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # GỌI MODEL ĐỂ LƯU VÀO DATABASE[cite: 14]
            if self.model.update_status(p['id'], new_status):
                QMessageBox.information(self.view, "Thành công", f"Đã cập nhật trạng thái cho {p['ten_sp']}")
                # LOAD LẠI DỮ LIỆU ĐỂ NÚT ĐỔI MÀU[cite: 14, 15]
                self.load_data()
            else:
                QMessageBox.critical(self.view, "Lỗi", "Không thể cập nhật trạng thái vào cơ sở dữ liệu!")

    def handle_add(self):
        QMessageBox.information(self.view, "Thông báo", "Mở form thêm sản phẩm mới")