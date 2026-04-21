from config.database import get_connection


class NvNhapHangController:
    def __init__(self):
        self.conn = get_connection()

    # ===== LẤY SẢN PHẨM =====
    def get_sanpham(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM san_pham")
        return cursor.fetchall()

    # ===== LẤY NHÀ CUNG CẤP =====
    def get_nhacungcap(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM nha_cung_cap")
        return cursor.fetchall()
     
     
    # ===== THÊM PHIẾU NHẬP =====
    def them_phieu_nhap(self, id_nhan_vien, id_ncc, danh_sach_sp):
        cursor = self.conn.cursor()

        try:
            # 👉 validate
            if not danh_sach_sp:
                raise Exception("Danh sách sản phẩm rỗng")

            if id_nhan_vien is None or id_ncc is None:
                raise Exception("Thiếu nhân viên hoặc nhà cung cấp")

            # 👉 tính tổng tiền
            tong_tien = sum(
                (sp["so_luong"] or 0) * (sp["gia"] or 0)
                for sp in danh_sach_sp
            )

            # 👉 insert bảng nhap_hang
            cursor.execute("""
                INSERT INTO nhap_hang (ngay_nhap, id_nhan_vien, id_nha_cung_cap, tong_tien_nhap)
                VALUES (NOW(), %s, %s, %s)
            """, (id_nhan_vien, id_ncc, tong_tien))

            phieu_id = cursor.lastrowid

            # 👉 update tồn kho
            for sp in danh_sach_sp:
                cursor.execute("""
                    UPDATE san_pham
                    SET so_luong_ton = so_luong_ton + %s
                    WHERE id = %s
                """, (sp["so_luong"], sp["id"]))

            # 👉 commit
            self.conn.commit()

            return phieu_id  # trả về để dùng nếu cần

        except Exception as e:
            self.conn.rollback()  # rollback nếu lỗi
            raise e