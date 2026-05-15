import mysql.connector
from config.database import get_connection

class NhapHangModel:
    def get_import_history(self):
        """
        Lấy lịch sử nhập kho.
        Sử dụng GROUP_CONCAT để gộp các sản phẩm trong cùng một phiếu nhập 
        thành các dòng riêng biệt trong một ô.
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # SQL tối ưu: Tách Tên SP và ĐVT ra 2 cột riêng, mỗi SP một dòng
            sql = """
                SELECT 
                    n.id, 
                    n.ngay_nhap, 
                    ncc.ten_ncc, 
                    n.tong_tien_nhap, 
                    nv.ho_ten as ten_nv,
                    GROUP_CONCAT(s.ten_sp SEPARATOR '\n') as ds_ten_sp,
                    GROUP_CONCAT(IFNULL(d.ten_dvt, 'Kg') SEPARATOR '\n') as ds_dvt
                FROM nhap_hang n
                JOIN chi_tiet_nhap_hang ct ON n.id = ct.id_nhap_hang
                JOIN san_pham s ON ct.id_san_pham = s.id
                LEFT JOIN don_vi_tinh d ON s.id_dvt = d.id
                JOIN nha_cung_cap ncc ON n.id_nha_cung_cap = ncc.id
                JOIN nhan_vien nv ON n.id_nhan_vien = nv.id
                GROUP BY n.id
                ORDER BY n.ngay_nhap DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi SQL get_import_history: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_import_details(self, id_nhap):
        """Lấy chi tiết sản phẩm của một phiếu nhập cụ thể"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT ct.so_luong_nhap, ct.gia_nhap, ct.thanh_tien, sp.ten_sp, d.ten_dvt
                FROM chi_tiet_nhap_hang ct
                JOIN san_pham sp ON ct.id_san_pham = sp.id
                LEFT JOIN don_vi_tinh d ON sp.id_dvt = d.id
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

    def add_import_receipt(self, id_nhan_vien, id_ncc, tong_tien, danh_sach_sp):
        """Lưu phiếu nhập mới và cập nhật số lượng tồn kho"""
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()

            # 1. Thêm vào bảng nhap_hang
            cursor.execute("""
                INSERT INTO nhap_hang (ngay_nhap, id_nhan_vien, id_nha_cung_cap, tong_tien_nhap)
                VALUES (NOW(), %s, %s, %s)
            """, (id_nhan_vien, id_ncc, tong_tien))
            
            phieu_id = cursor.lastrowid

            # 2. Thêm chi tiết và cập nhật kho
            for sp in danh_sach_sp:
                # sp bao gồm: id (của sản phẩm), so_luong, gia
                thanh_tien = sp['so_luong'] * sp['gia']
                
                cursor.execute("""
                    INSERT INTO chi_tiet_nhap_hang (id_nhap_hang, id_san_pham, so_luong_nhap, gia_nhap, thanh_tien)
                    VALUES (%s, %s, %s, %s, %s)
                """, (phieu_id, sp['id'], sp['so_luong'], sp['gia'], thanh_tien))

                # Cập nhật số lượng tồn trong bảng san_pham
                cursor.execute("""
                    UPDATE san_pham 
                    SET so_luong_ton = so_luong_ton + %s 
                    WHERE id = %s
                """, (sp['so_luong'], sp['id']))

            conn.commit()
            return True
        except Exception as e:
            if conn: conn.rollback()
            print(f"Lỗi khi lưu phiếu nhập: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()