from config.database import get_connection

class BaoCaoModel:
    def get_dashboard_chart_data(self, filter_mode="7 Ngày gần nhất"):
        """
        Lấy dữ liệu thống kê dựa trên cấu trúc database cuahang_nongsan
        """
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Xác định query dựa trên chế độ lọc
            if filter_mode == "Theo Tuần":
                # Nhóm theo tuần sử dụng YEARWEEK
                query = """
                    SELECT 
                        YEARWEEK(ngay_lap) as key_date, 
                        DATE_FORMAT(MIN(ngay_lap), 'Tuần %u') as label,
                        SUM(tong_tien) as doanh_thu, 
                        COUNT(id) as so_don,
                        (SELECT SUM(so_luong_huy) FROM thanh_ly_huy_hang 
                         WHERE YEARWEEK(ngay_huy) = YEARWEEK(h.ngay_lap)) as hang_huy
                    FROM hoa_don h 
                    WHERE ngay_lap >= DATE_SUB(CURDATE(), INTERVAL 8 WEEK)
                    GROUP BY key_date ORDER BY key_date ASC
                """
            elif filter_mode == "Theo Tháng":
                # Nhóm theo tháng sử dụng DATE_FORMAT
                query = """
                    SELECT 
                        DATE_FORMAT(ngay_lap, '%Y-%m') as key_date, 
                        DATE_FORMAT(ngay_lap, 'Tháng %m') as label,
                        SUM(tong_tien) as doanh_thu, 
                        COUNT(id) as so_don,
                        (SELECT SUM(so_luong_huy) FROM thanh_ly_huy_hang 
                         WHERE DATE_FORMAT(ngay_huy, '%Y-%m') = DATE_FORMAT(h.ngay_lap, '%Y-%m')) as hang_huy
                    FROM hoa_don h 
                    WHERE ngay_lap >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                    GROUP BY key_date ORDER BY key_date ASC
                """
            else:
                # Mặc định 7 ngày gần nhất, dùng cột ngay_lap
                query = """
                    SELECT 
                        DATE(ngay_lap) as key_date, 
                        DATE_FORMAT(ngay_lap, '%d/%m') as label,
                        SUM(tong_tien) as doanh_thu, 
                        COUNT(id) as so_don,
                        (SELECT SUM(so_luong_huy) FROM thanh_ly_huy_hang 
                         WHERE DATE(ngay_huy) = DATE(h.ngay_lap)) as hang_huy
                    FROM hoa_don h 
                    WHERE ngay_lap >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                    GROUP BY key_date ORDER BY key_date ASC
                """

            cursor.execute(query)
            res = cursor.fetchall()
            conn.close()
            return res
        except Exception as e:
            print(f"Lỗi SQL Dashboard: {e}")
            return []

    def get_kpi_totals(self):
        """Lấy các chỉ số tổng hợp cho các thẻ KPI Card"""
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # 1. Doanh thu hôm nay[cite: 9]
            cursor.execute("SELECT SUM(tong_tien) as t FROM hoa_don WHERE DATE(ngay_lap) = CURDATE()")
            rev = cursor.fetchone()['t'] or 0
            
            # 2. Đơn hàng mới (Chờ xử lý - trang_thai_giao = 0)[cite: 9]
            cursor.execute("SELECT COUNT(*) as t FROM hoa_don WHERE trang_thai_giao = 0")
            ords = cursor.fetchone()['t'] or 0
            
            # 3. Sản phẩm sắp hết hàng (so_luong_ton < 10)[cite: 9]
            cursor.execute("SELECT COUNT(*) as t FROM san_pham WHERE so_luong_ton < 10")
            stock = cursor.fetchone()['t'] or 0
            
            # 4. Hàng hủy hôm nay[cite: 9]
            cursor.execute("SELECT SUM(so_luong_huy) as t FROM thanh_ly_huy_hang WHERE DATE(ngay_huy) = CURDATE()")
            waste = cursor.fetchone()['t'] or 0
            
            conn.close()
            return rev, ords, stock, waste
        except Exception as e:
            print(f"Lỗi KPI: {e}")
            return 0, 0, 0, 0