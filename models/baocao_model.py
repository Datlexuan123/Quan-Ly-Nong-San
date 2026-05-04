def get_dashboard_chart_data(self):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Lấy dữ liệu trong 7 ngày gần nhất
    query = """
        SELECT 
            DATE(ngay_tao) as ngay,
            SUM(tong_tien) as doanh_thu,
            COUNT(id) as so_don_hang,
            (SELECT SUM(so_luong_huy) FROM thanh_ly_huy_hang 
             WHERE DATE(ngay_huy) = DATE(h.ngay_tao) AND trang_thai = 1) as hang_huy
        FROM hoa_don h
        WHERE ngay_tao >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        GROUP BY DATE(ngay_tao)
        ORDER BY ngay ASC
    """
    cursor.execute(query)
    res = cursor.fetchall()
    conn.close()
    return res