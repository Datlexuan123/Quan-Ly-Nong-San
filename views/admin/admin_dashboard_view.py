# views/admin/admin_dashboard_view.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QPushButton, QDialog, QTableWidget, 
    QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt6.QtCharts import (
    QChart, QChartView, QLineSeries, QValueAxis, QCategoryAxis
)
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
        self.layout.setSpacing(15)

        # --- 1. HEADER ---
        header_layout = QHBoxLayout()
        title_main = QLabel("📊 TỔNG QUAN HỆ THỐNG")
        title_main.setStyleSheet("font-size: 20px; font-weight: bold; color: #2e7d32;")
        
        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["7 Ngày gần nhất", "Theo Tuần", "Theo Tháng"])
        self.combo_filter.currentIndexChanged.connect(self.load_real_data)
        
        self.btn_refresh = QPushButton("🔄 Làm mới")
        self.btn_refresh.clicked.connect(self.load_real_data)
        
        header_layout.addWidget(title_main)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("Lọc:"))
        header_layout.addWidget(self.combo_filter)
        header_layout.addWidget(self.btn_refresh)
        self.layout.addLayout(header_layout)

        # --- 2. KPI CARDS ---
        card_layout = QHBoxLayout()
        self.card_rev, self.lbl_rev = self.create_card("DOANH THU", "0 VNĐ", "#2e7d32")
        self.card_ord, self.lbl_ord = self.create_card("ĐƠN HÀNG MỚI", "0", "#1565c0")
        self.card_stock, self.lbl_stock = self.create_card("SẮP HẾT HÀNG", "0 SP", "#d32f2f")
        self.card_waste, self.lbl_waste = self.create_card("HÀNG HỦY", "0 SP", "#f57c00")
        
        self.card_ord.mousePressEvent = self.open_order_detail
        self.card_stock.mousePressEvent = self.open_stock_detail
        self.card_waste.mousePressEvent = self.open_waste_detail
        
        for c in [self.card_rev, self.card_ord, self.card_stock, self.card_waste]:
            card_layout.addWidget(c)
        self.layout.addLayout(card_layout)

        # --- 3. BASIC LINE CHART ---
        self.chart = QChart()
        self.chart.setTitle("Biểu đồ doanh thu và đơn hàng")
        
        self.series_revenue = QLineSeries()
        self.series_revenue.setName("Doanh thu (VNĐ)")
        self.series_orders = QLineSeries()
        self.series_orders.setName("Số đơn hàng")

        self.chart.addSeries(self.series_revenue)
        self.chart.addSeries(self.series_orders)

        self.axis_x = QCategoryAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.series_revenue.attachAxis(self.axis_x)
        self.series_orders.attachAxis(self.axis_x)

        self.axis_y_left = QValueAxis()
        self.axis_y_left.setTitleText("VNĐ")
        self.chart.addAxis(self.axis_y_left, Qt.AlignmentFlag.AlignLeft)
        self.series_revenue.attachAxis(self.axis_y_left)

        self.axis_y_right = QValueAxis()
        self.axis_y_right.setTitleText("Đơn hàng")
        self.chart.addAxis(self.axis_y_right, Qt.AlignmentFlag.AlignRight)
        self.series_orders.attachAxis(self.axis_y_right)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.layout.addWidget(self.chart_view)

    def create_card(self, title, value, color):
        card = QFrame()
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setStyleSheet(f"background-color: {color}; border-radius: 8px; color: white;")
        card.setFixedHeight(90)
        l = QVBoxLayout(card)
        t = QLabel(title); t.setStyleSheet("font-size: 12px; font-weight: bold;")
        v = QLabel(value); v.setStyleSheet("font-size: 20px; font-weight: bold;")
        l.addWidget(t); l.addWidget(v)
        return card, v

    def show_detail_dialog(self, title, sql, headers):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(700, 400) # Tăng kích thước để hiện đủ thông tin
        l = QVBoxLayout(dialog)
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, val in enumerate(row.values()):
                    # Định dạng tiền tệ nếu là cột cuối (Tổng tiền)
                    text = f"{val:,.0f} VNĐ" if isinstance(val, (int, float)) and j == len(headers)-1 else str(val or "")
                    table.setItem(i, j, QTableWidgetItem(text))
            conn.close()
        except Exception as e: print(f"Lỗi hiển thị bảng: {e}")
        l.addWidget(table); dialog.exec()

    def open_order_detail(self, e):
        # SQL kết nối các bảng để lấy tên khách và chi tiết sản phẩm[cite: 7]
        query = """
            SELECT 
                h.id AS 'Mã đơn', 
                COALESCE(k.ho_ten, 'Khách lẻ') AS 'Khách hàng', 
                GROUP_CONCAT(CONCAT(s.ten_sp, ' (x', ct.so_luong, ')') SEPARATOR ', ') AS 'Chi tiết SP',
                h.tong_tien AS 'Tổng tiền'
            FROM hoa_don h
            LEFT JOIN khach_hang k ON h.id_khach_hang = k.id
            LEFT JOIN chi_tiet_hoa_don ct ON h.id = ct.id_hoa_don
            LEFT JOIN san_pham s ON ct.id_san_pham = s.id
            WHERE h.trang_thai_giao = 0
            GROUP BY h.id
        """
        self.show_detail_dialog("📑 Đơn hàng chờ xử lý", query, ["Mã đơn", "Khách hàng", "Chi tiết SP", "Tổng tiền"])

    def open_stock_detail(self, e):
        self.show_detail_dialog("📦 Sản phẩm sắp hết hàng", 
            "SELECT ten_sp, so_luong_ton FROM san_pham WHERE so_luong_ton < 10", ["Tên sản phẩm", "Số lượng tồn"])

    def open_waste_detail(self, e):
        # SQL lấy tên sản phẩm thay vì ID[cite: 7]
        query = """
            SELECT 
                s.ten_sp AS 'Sản phẩm', 
                t.so_luong_huy AS 'Số lượng', 
                t.ly_do AS 'Lý do hủy'
            FROM thanh_ly_huy_hang t
            JOIN san_pham s ON t.id_san_pham = s.id
            WHERE DATE(t.ngay_huy) = CURDATE()
        """
        self.show_detail_dialog("🗑️ Chi tiết hàng hủy hôm nay", query, ["Sản phẩm", "Số lượng", "Lý do hủy"])

    def load_real_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # Dùng đúng cột ngay_lap từ database của bạn[cite: 7, 11]
            cursor.execute("SELECT SUM(tong_tien) as t FROM hoa_don WHERE DATE(ngay_lap) = CURDATE()")
            self.lbl_rev.setText(f"{cursor.fetchone()['t'] or 0:,.0f} VNĐ")
            cursor.execute("SELECT COUNT(*) as t FROM hoa_don WHERE trang_thai_giao = 0")
            self.lbl_ord.setText(str(cursor.fetchone()['t']))
            cursor.execute("SELECT COUNT(*) as t FROM san_pham WHERE so_luong_ton < 10")
            self.lbl_stock.setText(f"{cursor.fetchone()['t']} SP")
            cursor.execute("SELECT SUM(so_luong_huy) as t FROM thanh_ly_huy_hang WHERE DATE(ngay_huy) = CURDATE()")
            self.lbl_waste.setText(f"{cursor.fetchone()['t'] or 0} SP")
            
            self.update_chart(cursor)
            conn.close()
        except Exception as e: print(f"Lỗi tải dữ liệu: {e}")

    def update_chart(self, cursor):
        mode = self.combo_filter.currentText()
        if mode == "Theo Tuần":
            q = "SELECT DATE_FORMAT(ngay_lap, 'Tuần %u') as l, SUM(tong_tien) as d, COUNT(id) as s FROM hoa_don GROUP BY l ORDER BY ngay_lap DESC LIMIT 8"
        elif mode == "Theo Tháng":
            q = "SELECT DATE_FORMAT(ngay_lap, 'Tháng %m') as l, SUM(tong_tien) as d, COUNT(id) as s FROM hoa_don GROUP BY l ORDER BY ngay_lap DESC LIMIT 6"
        else:
            q = "SELECT DATE_FORMAT(ngay_lap, '%d/%m') as l, SUM(tong_tien) as d, COUNT(id) as s FROM hoa_don WHERE ngay_lap >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) GROUP BY l ORDER BY ngay_lap ASC"

        cursor.execute(q)
        data = cursor.fetchall()
        
        self.series_revenue.clear(); self.series_orders.clear()
        for cat in self.axis_x.categoriesLabels(): self.axis_x.remove(cat)
        
        max_d = 1000; max_s = 5
        for i, row in enumerate(data):
            self.series_revenue.append(i, float(row['d'] or 0))
            self.series_orders.append(i, float(row['s'] or 0))
            self.axis_x.append(row['l'], i)
            max_d = max(max_d, float(row['d'] or 0))
            max_s = max(max_s, float(row['s'] or 0))
            
        self.axis_y_left.setRange(0, max_d * 1.2)
        self.axis_y_right.setRange(0, max_s + 2)
        self.axis_x.setRange(0, len(data) - 1 if data else 1)