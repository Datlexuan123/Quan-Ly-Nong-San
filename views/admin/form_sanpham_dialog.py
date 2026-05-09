from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, 
    QVBoxLayout, QLabel, QHBoxLayout, QFileDialog, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

class DragDropLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setPlaceholderText("Kéo ảnh vào đây hoặc nhấn nút chọn...")
        self.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 5px; background: #fafafa;")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            self.setText(path)
            if hasattr(self.parent(), 'update_preview'):
                self.parent().update_preview(path)

class FormSanPhamDialog(QDialog):
    def __init__(self, parent=None, du_lieu_cu=None):
        super().__init__(parent)
        self.du_lieu_cu = du_lieu_cu
        self.setWindowTitle("📦 THIẾT LẬP SẢN PHẨM")
        self.setFixedWidth(750) # Tăng độ rộng để chia 2 cột
        self.setStyleSheet("background-color: #ffffff; font-family: Arial;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # 1. TIÊU ĐỀ
        title = QLabel("NHẬP THÔNG TIN MỚI" if not self.du_lieu_cu else "CẬP NHẬT SẢN PHẨM")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1b5e20;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # KẺ NGANG
        line = QFrame(); line.setFrameShape(QFrame.Shape.HLine); line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # 2. BỐ CỤC CHÍNH (2 CỘT)
        content_layout = QHBoxLayout()
        
        # --- CỘT TRÁI: NHẬP LIỆU ---
        left_panel = QWidget()
        form = QFormLayout(left_panel)
        form.setSpacing(15)

        self.txt_ten = self.create_input("Nhập tên sản phẩm...")
        self.txt_gia = self.create_input("Ví dụ: 15000")
        self.txt_hsd = self.create_input("Ví dụ: 2027")
        self.txt_anh = DragDropLineEdit(self)
        self.txt_anh.textChanged.connect(self.update_preview)
        
        self.cbo_dvt = QComboBox()
        self.cbo_dvt.addItems(["Kg", "Bó", "Trái", "Hộp", "Túi"])
        self.cbo_dvt.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 5px;")

        form.addRow("<b>Tên sản phẩm:</b>", self.txt_ten)
        form.addRow("<b>Giá bán (VNĐ):</b>", self.txt_gia)
        form.addRow("<b>Hạn dùng (Năm):</b>", self.txt_hsd)
        form.addRow("<b>Đơn vị tính:</b>", self.cbo_dvt)
        
        # Dòng chọn ảnh
        box_anh = QHBoxLayout()
        box_anh.addWidget(self.txt_anh)
        btn_browse = QPushButton("Chọn File")
        btn_browse.setStyleSheet("padding: 8px; background: #e0e0e0; border-radius: 5px;")
        btn_browse.clicked.connect(self.mo_cua_so_chon_file)
        box_anh.addWidget(btn_browse)
        form.addRow("<b>Hình ảnh:</b>", box_anh)

        content_layout.addWidget(left_panel, 60) # Chiếm 60% chiều rộng

        # --- CỘT PHẢI: XEM TRƯỚC ẢNH ---
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        lbl_preview_title = QLabel("XEM TRƯỚC ẢNH")
        lbl_preview_title.setStyleSheet("font-weight: bold; color: #666;")
        right_panel.addWidget(lbl_preview_title)

        self.lbl_preview = QLabel()
        self.lbl_preview.setFixedSize(220, 220)
        self.lbl_preview.setStyleSheet("border: 2px dashed #bbb; border-radius: 10px; background: #f9f9f9;")
        self.lbl_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_preview.setText("Chưa có ảnh")
        right_panel.addWidget(self.lbl_preview)
        
        content_layout.addLayout(right_panel, 40) # Chiếm 40% chiều rộng

        main_layout.addLayout(content_layout)

        # 3. CỤM NÚT BẤM (DƯỚI CÙNG)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        self.btn_huy = QPushButton(" HỦY BỎ ")
        self.btn_huy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_huy.setStyleSheet("padding: 10px 25px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 5px;")
        self.btn_huy.clicked.connect(self.reject)
        
        self.btn_luu = QPushButton(" LƯU THÔNG TIN ")
        self.btn_luu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_luu.setStyleSheet("padding: 10px 35px; background: #2e7d32; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_luu.clicked.connect(self.accept)
        
        btn_row.addWidget(self.btn_huy)
        btn_row.addWidget(self.btn_luu)
        main_layout.addLayout(btn_row)

        # Đổ dữ liệu cũ
        if self.du_lieu_cu:
            self.txt_ten.setText(str(self.du_lieu_cu.get('ten_sp', '')))
            self.txt_ten.setEnabled(False)
            self.txt_gia.setText(str(self.du_lieu_cu.get('gia_ban', '')))
            self.txt_hsd.setText(str(self.du_lieu_cu.get('han_su_dung', '')))
            path = self.du_lieu_cu.get('hinh_anh', '')
            self.txt_anh.setText(path)
            self.update_preview(path)

    def create_input(self, placeholder):
        txt = QLineEdit()
        txt.setPlaceholderText(placeholder)
        txt.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 5px;")
        return txt

    def update_preview(self, path):
        if path:
            pix = QPixmap(path)
            if not pix.isNull():
                self.lbl_preview.setPixmap(pix.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                return
        self.lbl_preview.setText("Không tìm thấy ảnh")
        self.lbl_preview.setPixmap(QPixmap())

    def mo_cua_so_chon_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.txt_anh.setText(file_path)

    def lay_du_lieu(self):
        return {
            'ten': self.txt_ten.text(),
            'gia': self.txt_gia.text(),
            'hsd': self.txt_hsd.text(),
            'anh': self.txt_anh.text(),
            'dvt': self.cbo_dvt.currentIndex() + 1
        }

from PyQt6.QtWidgets import QWidget # Cần thêm cái này để chạy đúng layout