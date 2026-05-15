from config.database import get_connection
from models.nhaphang_model import NhapHangModel

class NvNhapHangController:
    def __init__(self):
        self.import_model = NhapHangModel()

    def ghi_log(self, id_nv, hanh_dong):
        """Hàm dùng chung để ghi lại lịch sử hoạt động hệ thống"""
        conn = None; cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO he_thong_log (id_nhan_vien, hanh_dong, thoi_gian) VALUES (%s, %s, NOW())"
            cursor.execute(sql, (id_nv, hanh_dong))
            conn.commit()
        except Exception as e:
            print(f"Lỗi ghi nhật ký: {e}")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def get_sanpham(self):
        conn = None; cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            # SỬA: Thêm JOIN để lấy ten_dvt
            sql = """
                SELECT s.id, s.ten_sp, s.so_luong_ton, d.ten_dvt 
                FROM san_pham s
                LEFT JOIN don_vi_tinh d ON s.id_dvt = d.id
            """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi lấy sản phẩm: {e}"); return []
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

    def get_import_history(self):

        """Cầu nối gọi dữ liệu lịch sử từ Model"""
        return self.import_model.get_import_history()

    def them_phieu_nhap(self, id_nhan_vien, id_ncc, danh_sach_sp):
        conn = None; cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            conn.start_transaction()

            tong_tien = sum((sp["so_luong"] * sp["gia"]) for sp in danh_sach_sp)

            cursor.execute("""
                INSERT INTO nhap_hang (ngay_nhap, id_nhan_vien, id_nha_cung_cap, tong_tien_nhap)
                VALUES (NOW(), %s, %s, %s)
            """, (id_nhan_vien, id_ncc, tong_tien))
            phieu_id = cursor.lastrowid

            for sp in danh_sach_sp:
                cursor.execute("""
                    INSERT INTO chi_tiet_nhap_hang (id_nhap_hang, id_san_pham, so_luong_nhap, gia_nhap, thanh_tien)
                    VALUES (%s, %s, %s, %s, %s)
                """, (phieu_id, sp["id"], sp["so_luong"], sp["gia"], sp["so_luong"] * sp["gia"]))

                cursor.execute("UPDATE san_pham SET so_luong_ton = so_luong_ton + %s WHERE id = %s", 
                               (sp["so_luong"], sp["id"]))

            conn.commit()
            
            # GHI LOG SAU KHI NHẬP HÀNG THÀNH CÔNG
            self.ghi_log(id_nhan_vien, f"Đã nhập phiếu hàng #{phieu_id} từ NCC ID {id_ncc}")
            
            return True
        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if cursor: cursor.close()
            if conn: conn.close()