import mysql.connector
from config.database import get_connection

class NhapHangModel:
    def get_import_history(self):
        """Lấy danh sách các lần nhập hàng kèm tổng số lượng nhập từ bảng chi tiết"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # COALESCE giúp chuyển các giá trị NULL thành 0 nếu chưa có chi tiết[cite: 11]
            query = """
                SELECT 
                    nh.id, 
                    nh.ngay_nhap, 
                    nh.tong_tien_nhap, 
                    ncc.ten_ncc, 
                    nv.ho_ten as ten_nv,
                    COALESCE(SUM(ct.so_luong_nhap), 0) as tong_sl_nhap
                FROM nhap_hang nh
                JOIN nha_cung_cap ncc ON nh.id_nha_cung_cap = ncc.id
                JOIN nhan_vien nv ON nh.id_nhan_vien = nv.id
                LEFT JOIN chi_tiet_nhap_hang ct ON nh.id = ct.id_nhap_hang
                GROUP BY nh.id
                ORDER BY nh.ngay_nhap DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy lịch sử nhập kho: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_import_details(self, id_nhap):
        """Lấy chi tiết sản phẩm (bao gồm Tên, SL, Giá) trong một phiếu nhập"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # JOIN với bảng san_pham để lấy cột ten_sp
            query = """
                SELECT ct.so_luong_nhap, ct.gia_nhap, ct.thanh_tien, sp.ten_sp 
                FROM chi_tiet_nhap_hang ct
                JOIN san_pham sp ON ct.id_san_pham = sp.id
                WHERE ct.id_nhap_hang = %s
            """
            cursor.execute(query, (id_nhap,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy chi tiết sản phẩm: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def ghi_log(self, id_nv, hanh_dong):
        """Hàm dùng chung để ghi lại lịch sử hoạt động"""
        conn = None; cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO he_thong_log (id_nhan_vien, hanh_dong, thoi_gian) VALUES (%s, %s, NOW())"
            cursor.execute(sql, (id_nv, hanh_dong))
            conn.commit()
        except Exception as e:
            print(f"Lỗi ghi log: {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()