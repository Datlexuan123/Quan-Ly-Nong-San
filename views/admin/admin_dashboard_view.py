# views/admin/admin_dashboard_view.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QPushButton, QSizePolicy, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QFont
from config.database import get_connection

class AdminDashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_real_data()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        # --- HEADER & REFRESH ---
        header_top_layout = QHBoxLayout()
        title_main = QLabel("📊 TỔNG QUAN HỆ THỐNG")
        title_main.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        self.btn_refresh = QPushButton("🔄 Làm mới dữ liệu")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.setFixedWidth(160)
        self.btn_refresh.clicked.connect(self.load_real_data)
        header_top_layout.addWidget(title_main)
        header_top_layout.addStretch()
        header_top_layout.addWidget(self.btn_refresh)
        self.layout.addLayout(header_top_layout)

        # 1. KPI CARDS - Thêm sự kiện Click cho từng hộp[cite: 8, 9]
        card_layout = QHBoxLayout()
        
        self.card_doanh_thu, self.lbl_value_doanh_thu = self.create_card("DOANH THU HÔM NAY", "0 VNĐ", "#2e7d32")
        self.card_don_hang, self.lbl_value_don_hang = self.create_card("ĐƠN HÀNG MỚI", "0", "#1565c0")
        self.card_canh_bao, self.lbl_value_canh_bao = self.create_card("SẮP HẾT HÀNG", "0 SP", "#d32f2f")
        self.card_hang_huy, self.lbl_value_hang_huy = self.create_card("HÀNG HỦY HÔM NAY", "0 SP", "#ff9800")
        
        # Thiết lập hiệu ứng bàn tay và sự kiện nhấn chuột
        for card in [self.card_doanh_thu, self.card_don_hang, self.card_canh_bao, self.card_hang_huy]:
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            
        self.card_don_hang.mousePressEvent = self.open_order_detail
        self.card_canh_bao.mousePressEvent = self.open_stock_detail
        self.card_hang_huy.mousePressEvent = self.open_waste_detail

        card_layout.addWidget(self.card_doanh_thu)
        card_layout.addWidget(self.card_don_hang)
        card_layout.addWidget(self.card_canh_bao)
        card_layout.addWidget(self.card_hang_huy)
        self.layout.addLayout(card_layout)

        # 2. BIỂU ĐỒ HAI TRỤC TUNG[cite: 8, 9]
        self.chart = QChart()
        self.chart.setTitle("XU HƯỚNG KINH DOANH (7 NGÀY)")
        
        self.series_revenue = QLineSeries(); self.series_revenue.setName("Doanh thu (VNĐ)")
        self.series_orders = QLineSeries(); self.series_orders.setName("Số đơn hàng")
        self.series_waste = QLineSeries(); self.series_waste.setName("Hàng hủy")

        self.chart.addSeries(self.series_revenue)
        self.chart.addSeries(self.series_orders)
        self.chart.addSeries(self.series_waste)

        axis_font = QFont("Arial", 12, QFont.Weight.Bold)

        self.axis_x = QCategoryAxis()
        self.axis_x.setLabelsFont(axis_font)
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)

        self.axis_y_left = QValueAxis()
        self.axis_y_left.setTitleText("Doanh thu (VNĐ)")
        self.axis_y_left.setLabelsFont(axis_font)
        self.axis_y_left.setLabelFormat("%d")
        self.chart.addAxis(self.axis_y_left, Qt.AlignmentFlag.AlignLeft)

        self.axis_y_right = QValueAxis()
        self.axis_y_right.setTitleText("Số lượng (SP/Đơn)")
        self.axis_y_right.setLabelsFont(axis_font)
        self.axis_y_right.setLabelFormat("%d")
        self.chart.addAxis(self.axis_y_right, Qt.AlignmentFlag.AlignRight)

        self.series_revenue.attachAxis(self.axis_x)
        self.series_revenue.attachAxis(self.axis_y_left)
        self.series_orders.attachAxis(self.axis_x)
        self.series_orders.attachAxis(self.axis_y_right)
        self.series_waste.attachAxis(self.axis_x)
        self.series_waste.attachAxis(self.axis_y_right)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.layout.addWidget(self.chart_view, stretch=1)

    def create_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"background-color: {color}; border-radius: 10px; color: white;")
        card.setFixedHeight(115)
        l = QVBoxLayout(card)
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 11px; font-weight: bold; border: none;")
        v_lbl = QLabel(value)
        v_lbl.setStyleSheet("font-size: 20px; font-weight: bold; border: none;")
        l.addWidget(t_lbl)
        l.addWidget(v_lbl)
        return card, v_lbl

    # --- CÁC HÀM MỞ FORM CHI TIẾT ---[cite: 8]
    def open_stock_detail(self, event):
        """Mở chi tiết sản phẩm sắp hết hàng"""
        self.show_detail_dialog("Sản phẩm sắp hết hàng", 
            "SELECT ten_sp, so_luong_ton FROM san_pham WHERE so_luong_ton < 10",
            ["Tên sản phẩm", "Số lượng tồn"])

    def open_order_detail(self, event):
        """Mở chi tiết đơn hàng mới hôm nay"""
        self.show_detail_dialog("Đơn hàng mới chờ xử lý", 
            "SELECT id, tong_tien FROM hoa_don WHERE trang_thai_giao = 0",
            ["Mã hóa đơn", "Tổng tiền"])

    def open_waste_detail(self, event):
        """Mở chi tiết hàng hủy hôm nay"""
        self.show_detail_dialog("Chi tiết hàng hủy hôm nay", 
            "SELECT id_san_pham, so_luong_huy, ly_do FROM thanh_ly_huy_hang WHERE DATE(ngay_huy) = CURDATE()",
            ["ID Sản phẩm", "Số lượng", "Lý do"])

    def show_detail_dialog(self, title, sql, headers):
        """Hàm chung để tạo cửa sổ hiển thị bảng dữ liệu[cite: 8]"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(400, 300)
        layout = QVBoxLayout(dialog)
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, val in enumerate(row.values()):
                    table.setItem(i, j, QTableWidgetItem(str(val)))
            conn.close()
        except Exception as e: print(f"Lỗi tải chi tiết: {e}")
        
        layout.addWidget(table)
        dialog.exec()

    def load_real_data(self):
        """Cập nhật dữ liệu KPI[cite: 8, 9]"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT SUM(tong_tien) as total FROM hoa_don WHERE DATE(ngay_lap) = CURDATE()")
            self.lbl_value_doanh_thu.setText(f"{cursor.fetchone()['total'] or 0:,.0f} VNĐ")
            cursor.execute("SELECT COUNT(*) as total FROM hoa_don WHERE trang_thai_giao = 0")
            self.lbl_value_don_hang.setText(str(cursor.fetchone()['total']))
            cursor.execute("SELECT COUNT(*) as total FROM san_pham WHERE so_luong_ton < 10")
            self.lbl_value_canh_bao.setText(f"{cursor.fetchone()['total']} SP")
            cursor.execute("SELECT SUM(so_luong_huy) as total FROM thanh_ly_huy_hang WHERE DATE(ngay_huy) = CURDATE()")
            self.lbl_value_hang_huy.setText(f"{cursor.fetchone()['total'] or 0} SP")
            self.update_chart_data(cursor)
            conn.close()
        except Exception as e: print(f"Lỗi Dashboard: {e}")

    def update_chart_data(self, cursor):
        """Cập nhật biểu đồ[cite: 8, 9]"""
        query = """
            SELECT DATE(ngay_lap) as ngay, SUM(tong_tien) as doanh_thu,
            COUNT(id) as so_don, (SELECT SUM(so_luong_huy) FROM thanh_ly_huy_hang 
            WHERE DATE(ngay_huy) = DATE(h.ngay_lap)) as hang_huy
            FROM hoa_don h WHERE ngay_lap >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(ngay_lap) ORDER BY ngay ASC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        self.series_revenue.clear(); self.series_orders.clear(); self.series_waste.clear()
        for cat in self.axis_x.categoriesLabels(): self.axis_x.remove(cat)

        max_rev = 1000; max_small = 5 
        for i, row in enumerate(data):
            d_str = row['ngay'].strftime("%d/%m")
            rev, ords, wast = float(row['doanh_thu'] or 0), float(row['so_don'] or 0), float(row['hang_huy'] or 0)
            self.series_revenue.append(i, rev); self.series_orders.append(i, ords); self.series_waste.append(i, wast)
            self.axis_x.append(d_str, i)
            max_rev = max(max_rev, rev); max_small = max(max_small, ords, wast)

        self.axis_y_left.setRange(0, max_rev * 1.2) 
        self.axis_y_right.setRange(0, max_small + 2) 
        self.axis_x.setRange(0, len(data) - 1 if data else 1)