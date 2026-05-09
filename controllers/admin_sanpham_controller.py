# controllers/admin_sanpham_controller.py

from PyQt6.QtWidgets import (
    QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, 
    QMessageBox, QLabel, QDialog, QVBoxLayout, QHeaderView, QTableWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor, QFont
from matplotlib import container
from models.sanpham_model import SanPhamModel
# Import Form Dialog để dùng cho Thêm/Sửa
from views.admin.form_sanpham_dialog import FormSanPhamDialog

class AdminSanPhamController:
    def __init__(self, view, user_data=None):
        self.view = view
        self.user_data = user_data if user_data else {}
        self.model = SanPhamModel()
        
        # Kết nối sự kiện
        self.view.txt_search.textChanged.connect(self.load_data)
        self.view.btn_add.clicked.connect(self.handle_add)
        self.view.table.cellClicked.connect(self.handle_cell_click)
        
        # Cấu hình độ rộng cột cơ bản
        self.view.table.setColumnWidth(0, 55) 
        self.view.table.setColumnWidth(1, 90) 
        
        self.load_data()

   # controllers/admin_sanpham_controller.py

    def load_data(self):
        try:
            tu_khoa = self.view.txt_search.text().lower()
            products = self.model.get_all(tu_khoa)
            
            self.view.table.setRowCount(0)
            self.view.table.verticalHeader().setDefaultSectionSize(75)
            
            for row, p in enumerate(products):
                self.view.table.insertRow(row)
                
                # 0. MÃ SP, 1. HÌNH ẢNH, 2. TÊN SP (Giữ nguyên)
                self.view.table.setItem(row, 0, QTableWidgetItem(str(p['id'])))
                
                lbl_anh = QLabel()
                path = p.get('hinh_anh') or "images/no_image.png"
                pix = QPixmap(path)
                if pix.isNull(): pix = QPixmap("images/no_image.png")
                lbl_anh.setPixmap(pix.scaled(65, 65, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                lbl_anh.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.table.setCellWidget(row, 1, lbl_anh)

                item_ten = QTableWidgetItem(p['ten_sp'])
                item_ten.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                item_ten.setForeground(QColor("#007bff")) 
                self.view.table.setItem(row, 2, item_ten)

                # 3. MỚI: GIÁ VỐN TRUNG BÌNH
                gia_von = float(p.get('gia_von_tb') or 0)
                item_von = QTableWidgetItem(f"{gia_von:,.0f} đ")
                item_von.setForeground(QColor("#757575")) # Màu xám cho dễ phân biệt
                item_von.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.view.table.setItem(row, 3, item_von)

                # 4. GIÁ BÁN (Dịch sang cột 4)
                gia_ban = float(p.get('gia_ban', 0))
                item_ban = QTableWidgetItem(f"{gia_ban:,.0f} đ")
                item_ban.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.view.table.setItem(row, 4, item_ban)
                
                # 5. SỐ LƯỢNG TỒN (Dịch sang cột 5)
                ton = p.get('so_luong_ton', 0)
                item_ton = QTableWidgetItem(str(ton))
                if ton < 20: 
                    item_ton.setForeground(QColor("#d32f2f"))
                self.view.table.setItem(row, 5, item_ton)
                
                # 6. HẠN DÙNG, 7. ĐƠN VỊ TÍNH
                self.view.table.setItem(row, 6, QTableWidgetItem(str(p.get('han_su_dung') or "2027")))
                self.view.table.setItem(row, 7, QTableWidgetItem(p.get('ten_dvt') or "Kg"))

                # 8. THAO TÁC (Dịch sang cột 8)
                self.add_action_buttons(row, p)
                
        except Exception as e:
            print(f"Lỗi load sản phẩm: {e}")

    def add_action_buttons(self, row, p):
        # ... (Giữ nguyên phần tạo nút) ...
        # SỬA: Đổi chỉ số cột từ 7 thành 8
        self.view.table.setCellWidget(row, 8, container)

    def add_action_buttons(self, row, p):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Nút Sửa
        btn_edit = QPushButton("✏️")
        btn_edit.setFixedSize(30, 30)
        btn_edit.setStyleSheet("background-color: #ffb300; color: white; border-radius: 5px; border: none;")
        btn_edit.clicked.connect(lambda: self.handle_edit(p))
        
        # Nút Xóa
        btn_delete = QPushButton("🗑️")
        btn_delete.setFixedSize(30, 30)
        btn_delete.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; border: none;")
        btn_delete.clicked.connect(lambda: self.handle_delete(p))

        # Nút Trạng thái (Ẩn/Hiện sản phẩm)
        status = p.get('trang_thai', 0)
        btn_status = QPushButton("✅" if status == 0 else "🚫")
        btn_status.setFixedSize(30, 30)
        btn_status.setStyleSheet(f"background-color: {'#4caf50' if status == 0 else '#9e9e9e'}; border-radius: 5px; border: none;")
        btn_status.clicked.connect(lambda: self.toggle_product_status(p))

        layout.addWidget(btn_edit)
        layout.addWidget(btn_status)
        layout.addWidget(btn_delete)
        self.view.table.setCellWidget(row, 8, container)

    def handle_add(self):
        """Mở Form Tiếng Việt để thêm sản phẩm"""
        dialog = FormSanPhamDialog(self.view)
        if dialog.exec():
            data = dialog.lay_du_lieu()
            if self.model.add_product(data):
                QMessageBox.information(self.view, "Thành công", "Đã thêm sản phẩm mới!")
                self.load_data()

    def handle_edit(self, p):
        """Mở Form Tiếng Việt để sửa (Chỉ sửa Giá, Ảnh, ĐVT)"""
        dialog = FormSanPhamDialog(self.view, du_lieu_cu=p)
        if dialog.exec():
            data = dialog.lay_du_lieu()
            if self.model.update_product(p['id'], data):
                QMessageBox.information(self.view, "Thành công", "Đã cập nhật sản phẩm!")
                self.load_data()

    def handle_delete(self, p):
        """Xử lý xóa: Chặn nếu tồn kho > 0"""
        ten_sp = p['ten_sp']
        ton_kho = float(p.get('so_luong_ton', 0))

        if ton_kho > 0:
            QMessageBox.warning(self.view, "Không thể xóa", 
                                f"Sản phẩm '{ten_sp}' vẫn còn tồn kho ({ton_kho}).\nVui lòng xử lý hàng tồn trước khi xóa!")
            return

        confirm = QMessageBox.question(self.view, "Xác nhận xóa", 
                                     f"Bạn có chắc muốn xóa vĩnh viễn '{ten_sp}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            if self.model.delete_product(p['id']):
                QMessageBox.information(self.view, "Thành công", "Đã xóa sản phẩm!")
                self.load_data()

    def handle_cell_click(self, row, column):
        """Nhấn vào tên sản phẩm để xem lịch sử nhập hàng"""
        if column == 2: 
            try:
                product_id = self.view.table.item(row, 0).text()
                product_name = self.view.table.item(row, 2).text()
                history = self.model.get_import_history(product_id)
                if history:
                    self.show_history_dialog(product_name, history)
                else:
                    QMessageBox.information(self.view, "Thông báo", f"Sản phẩm '{product_name}' chưa có lịch sử nhập.")
            except Exception as e: print(f"Lỗi xem lịch sử: {e}")

    def show_history_dialog(self, name, data):
        dialog = QDialog(self.view)
        dialog.setWindowTitle(f"Lịch sử nhập: {name}")
        dialog.setMinimumSize(650, 450)
        layout = QVBoxLayout(dialog)
          
        # Lấy giá vốn trung bình từ dòng đầu tiên (nếu có dữ liệu)
        gia_tb_text = "0 đ"
        if data:
            gia_tb = float(data[0].get('gia_von_tb') or 0)
            gia_tb_text = f"{gia_tb:,.0f} đ"

        # Hiển thị con số giá vốn trung bình nổi bật ở trên bảng
        lbl_avg = QLabel(f"GIÁ VỐN TRUNG BÌNH HIỆN TẠI: {gia_tb_text}")
        lbl_avg.setStyleSheet("font-size: 14px; font-weight: bold; color: #d32f2f; margin-bottom: 10px;")
        layout.addWidget(lbl_avg)
        
        table = QTableWidget()
        table.setColumnCount(4)
        # Sửa tiêu đề cột thứ 3 thành "Giá Nhập (Gốc)" để phân biệt
        table.setHorizontalHeaderLabels(["Ngày Nhập", "Số Lượng", "Giá Nhập (Gốc)", "NCC"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        table.setRowCount(len(data))
        for i, h in enumerate(data):
            table.setItem(i, 0, QTableWidgetItem(str(h['ngay_nhap'])))
            table.setItem(i, 1, QTableWidgetItem(str(h['so_luong_nhap'])))
            
            # Giá nhập của từng lô cụ thể
            gia_lo = float(h['gia_nhap'] or 0)
            table.setItem(i, 2, QTableWidgetItem(f"{gia_lo:,.0f} đ"))
            
            table.setItem(i, 3, QTableWidgetItem(h.get('ten_ncc', 'N/A')))
        
        layout.addWidget(table)
        btn = QPushButton("Đóng"); btn.clicked.connect(dialog.close)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignRight)
        dialog.exec()