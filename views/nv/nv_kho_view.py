import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QComboBox, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from controllers.nv_nhaphang_controller import NvNhapHangController

class NvKhoView(QWidget):
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data if user_data else {}
        self.controller = NvNhapHangController()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        header = QLabel("📦 QUẢN LÝ KHO & NHẬP HÀNG")
        header.setStyleSheet("font-size:22px; font-weight:bold; color:#2e7d32;")
        main_layout.addWidget(header)

        top_frame = QFrame()
        top_frame.setStyleSheet("background:#f5f5f5; border-radius:10px; padding:10px;")
        top_layout = QHBoxLayout(top_frame)

        top_layout.addWidget(QLabel("Nhà cung cấp:"))
        self.cbo_ncc = QComboBox()
        self.cbo_ncc.setFixedWidth(250)
        top_layout.addWidget(self.cbo_ncc)

        ten_nv = self.user_data.get('ho_ten', 'Chưa xác định')
        self.lbl_nv = QLabel(f"👤 Nhân viên: <b>{ten_nv}</b>")
        self.lbl_nv.setStyleSheet("font-size: 14px; margin-left: 20px;")
        top_layout.addWidget(self.lbl_nv)

        top_layout.addStretch()
        main_layout.addWidget(top_frame)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tên sản phẩm", "Tồn kho", "Số lượng nhập", "Giá nhập"])
        self.table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table)

        self.btn_save = QPushButton("💾 XÁC NHẬN NHẬP HÀNG")
        self.btn_save.setFixedHeight(45)
        self.btn_save.setStyleSheet("background-color:#2e7d32; color:white; font-weight:bold;")
        # Kết nối sự kiện
        self.btn_save.clicked.connect(self.save_nhap_hang) 
        main_layout.addWidget(self.btn_save)

        self.load_data_to_form()

    def load_data_to_form(self):
        try:
            nccs = self.controller.get_nhacungcap()
            self.cbo_ncc.clear()
            for ncc in nccs:
                self.cbo_ncc.addItem(ncc['ten_ncc'], ncc['id'])

            products = self.controller.get_sanpham()
            self.table.setRowCount(len(products))
            for row, p in enumerate(products):
                self.table.setItem(row, 0, QTableWidgetItem(str(p["id"])))
                self.table.setItem(row, 1, QTableWidgetItem(p["ten_sp"])) 
                self.table.setItem(row, 2, QTableWidgetItem(str(p["so_luong_ton"])))

                spin_qty = QSpinBox()
                spin_qty.setRange(0, 10000)
                self.table.setCellWidget(row, 3, spin_qty)

                spin_price = QSpinBox()
                spin_price.setRange(0, 100000000)
                spin_price.setSingleStep(1000)
                self.table.setCellWidget(row, 4, spin_price)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {e}")

    # --- HÀM BỔ SUNG ĐỂ SỬA LỖI ---
    def save_nhap_hang(self):
        id_ncc = self.cbo_ncc.currentData()
        id_nv = self.user_data.get('id', 1)
        danh_sach_sp = []

        for row in range(self.table.rowCount()):
            qty = self.table.cellWidget(row, 3).value()
            price = self.table.cellWidget(row, 4).value()
            
            if qty > 0:
                id_sp = int(self.table.item(row, 0).text())
                danh_sach_sp.append({
                    "id": id_sp,
                    "so_luong": qty,
                    "gia": price
                })

        if not danh_sach_sp:
            QMessageBox.warning(self, "Chú ý", "Vui lòng nhập số lượng cho ít nhất 1 sản phẩm!")
            return

        try:
            # Gọi controller lưu vào DB
            if self.controller.them_phieu_nhap(id_nv, id_ncc, danh_sach_sp):
                QMessageBox.information(self, "Thành công", "Đã nhập hàng và cập nhật kho!")
                self.load_data_to_form() # Load lại bảng để cập nhật tồn kho mới
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu: {e}")