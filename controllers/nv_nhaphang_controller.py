from config.database import get_connection

class NvNhapHangController:
    def get_sanpham(self):
        conn = None; cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, ten_sp, so_luong_ton FROM san_pham")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi: {e}"); return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_nhacungcap(self):
        conn = None; cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, ten_ncc FROM nha_cung_cap")
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi: {e}"); return []
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def them_phieu_nhap(self, id_nhan_vien, id_ncc, danh_sach_sp):
        conn = None; cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()

            tong_tien = sum((sp["so_luong"] * sp["gia"]) for sp in danh_sach_sp)

            # 1. Insert bảng nhap_hang
            cursor.execute("""
                INSERT INTO nhap_hang (ngay_nhap, id_nhan_vien, id_nha_cung_cap, tong_tien_nhap)
                VALUES (NOW(), %s, %s, %s)
            """, (id_nhan_vien, id_ncc, tong_tien))
            phieu_id = cursor.lastrowid

            # 2. Insert chi tiết và Update kho
            for sp in danh_sach_sp:
                cursor.execute("""
                    INSERT INTO chi_tiet_nhap_hang (id_nhap_hang, id_san_pham, so_luong_nhap, gia_nhap, thanh_tien)
                    VALUES (%s, %s, %s, %s, %s)
                """, (phieu_id, sp["id"], sp["so_luong"], sp["gia"], sp["so_luong"] * sp["gia"]))

                cursor.execute("UPDATE san_pham SET so_luong_ton = so_luong_ton + %s WHERE id = %s", 
                               (sp["so_luong"], sp["id"]))

            conn.commit()
            return True
        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if cursor: cursor.close()
            if conn: conn.close()