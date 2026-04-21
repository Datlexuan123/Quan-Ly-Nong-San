import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QSpinBox, QComboBox, QMessageBox, QFrame, QApplication
)
from PyQt6.QtCore import Qt

from controllers.nv_nhaphang_controller import NvNhapHangController


class NvKhoView(QWidget):
    def __init__(self):
        super().__init__()

        self.controller = NvNhapHangController()

        # ===== LAYOUT CHÍNH =====
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ===== HEADER =====
        header = QLabel("📦 QUẢN LÝ KHO & NHẬP HÀNG")
        header.setStyleSheet("font-size:22px; font-weight:bold; color:#2e7d32;")
        main_layout.addWidget(header)

        # ===== KHUNG TRÊN =====
        top_frame = QFrame()
        top_frame.setStyleSheet("background:#f5f5f5; border-radius:10px; padding:10px;")

        top_layout = QHBoxLayout(top_frame)

        # Nhà cung cấp
        self.cbo_ncc = QComboBox()
        self.cbo_ncc.setFixedWidth(300)

        # Nhân viên
        self.cbo_nv = QComboBox()
        self.cbo_nv.setFixedWidth(200)

        top_layout.addWidget(QLabel("Nhà cung cấp:"))
        top_layout.addWidget(self.cbo_ncc)

        top_layout.addSpacing(20)

        top_layout.addWidget(QLabel("Nhân viên nhập:"))
        top_layout.addWidget(self.cbo_nv)

        top_layout.addStretch()

        main_layout.addWidget(top_frame)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Tên sản phẩm", "Tồn kho", "Số lượng nhập", "Giá nhập"
        ])

        self.table.setStyleSheet("""
            QTableWidget {
                background: white;
                border-radius: 10px;
                gridline-color: #ddd;
            }
        """)

        main_layout.addWidget(self.table)

        # ===== BUTTON =====
        self.btn_save = QPushButton("💾 XÁC NHẬN NHẬP HÀNG")
        self.btn_save.setFixedHeight(45)
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
        """)

        main_layout.addWidget(self.btn_save)

        # ===== LOAD DATA =====
        self.load_data()

        # ===== EVENT =====
        self.btn_save.clicked.connect(self.save_nhap_hang)

    # ======================================================
    # LOAD DỮ LIỆU
    # ======================================================
    def load_data(self):
        products = self.controller.get_sanpham()
        nccs = self.controller.get_nhacungcap()

        # ===== LOAD NCC =====
        self.cbo_ncc.clear()
        for ncc in nccs:
            text = f"{ncc['ten_ncc']} | {ncc['so_dien_thoai']}"
            self.cbo_ncc.addItem(text, ncc["id"])

        # ===== LOAD NHÂN VIÊN (tạm) =====
        self.cbo_nv.clear()
        self.cbo_nv.addItem("Nhân viên 1", 1)
        self.cbo_nv.addItem("Nhân viên 2", 2)

        # ===== LOAD TABLE =====
        self.table.setRowCount(len(products))

        for row, p in enumerate(products):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(p["id"])))

            # Tên
            self.table.setItem(row, 1, QTableWidgetItem(p["ten_sp"]))

            # Tồn kho
            self.table.setItem(row, 2, QTableWidgetItem(str(p["so_luong_ton"])))

            # Số lượng nhập
            spin = QSpinBox()
            spin.setMaximum(10000)
            spin.setStyleSheet("padding:3px;")
            self.table.setCellWidget(row, 3, spin)

            # Giá nhập
            price = QSpinBox()
            price.setMaximum(100000000)
            price.setStyleSheet("padding:3px;")
            self.table.setCellWidget(row, 4, price)

    # ======================================================
    # LƯU NHẬP HÀNG
    # ======================================================
    def save_nhap_hang(self):
        danh_sach = []

        for row in range(self.table.rowCount()):
            sp_id = int(self.table.item(row, 0).text())
            so_luong = self.table.cellWidget(row, 3).value()
            gia = self.table.cellWidget(row, 4).value()

            if so_luong > 0:
                danh_sach.append({
                    "id": sp_id,
                    "so_luong": so_luong,
                    "gia": gia
                })

        # ===== VALIDATE =====
        if not danh_sach:
            QMessageBox.warning(self, "Lỗi", "Bạn chưa nhập sản phẩm nào!")
            return

        id_ncc = self.cbo_ncc.currentData()
        id_nv = self.cbo_nv.currentData()

        try:
            self.controller.them_phieu_nhap(id_nv, id_ncc, danh_sach)

            QMessageBox.information(self, "Thành công", "Nhập hàng thành công!")

            # reload lại dữ liệu
            self.load_data()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))