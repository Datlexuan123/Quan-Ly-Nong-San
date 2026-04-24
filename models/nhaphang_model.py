import mysql.connector
from config.database import get_connection

class NhapHangModel:
    def get_import_history(self):
        """Lấy danh sách các lần nhập hàng an toàn"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT nh.id, nh.ngay_nhap, nh.tong_tien_nhap, ncc.ten_ncc, nv.ho_ten as ten_nv
                FROM nhap_hang nh
                JOIN nha_cung_cap ncc ON nh.id_nha_cung_cap = ncc.id
                JOIN nhan_vien nv ON nh.id_nhan_vien = nv.id
                ORDER BY nh.ngay_nhap DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy lịch sử: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_import_details(self, id_nhap):
        """Lấy chi tiết sản phẩm trong phiếu nhập"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT ct.*, sp.ten_sp 
                FROM chi_tiet_nhap_hang ct
                JOIN san_pham sp ON ct.id_san_pham = sp.id
                WHERE ct.id_nhap_hang = %s
            """
            cursor.execute(query, (id_nhap,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy chi tiết: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()