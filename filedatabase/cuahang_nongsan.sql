-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th4 21, 2026 lúc 06:45 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `cuahang_nongsan`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `chi_tiet_hoa_don`
--

CREATE TABLE `chi_tiet_hoa_don` (
  `id_hoa_don` int(11) NOT NULL,
  `id_san_pham` int(11) NOT NULL,
  `so_luong` float NOT NULL,
  `don_gia` decimal(15,2) NOT NULL,
  `thanh_tien` decimal(15,2) GENERATED ALWAYS AS (`so_luong` * `don_gia`) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `chi_tiet_nhap_hang`
--

CREATE TABLE `chi_tiet_nhap_hang` (
  `id_nhap_hang` int(11) NOT NULL,
  `id_san_pham` int(11) NOT NULL,
  `so_luong_nhap` float NOT NULL,
  `gia_nhap` decimal(15,2) NOT NULL,
  `thanh_tien` decimal(15,2) GENERATED ALWAYS AS (`so_luong_nhap` * `gia_nhap`) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `danh_muc`
--

CREATE TABLE `danh_muc` (
  `id` int(11) NOT NULL,
  `ten_danh_muc` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `don_vi_tinh`
--

CREATE TABLE `don_vi_tinh` (
  `id` int(11) NOT NULL,
  `ten_dvt` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `hoa_don`
--

CREATE TABLE `hoa_don` (
  `id` int(11) NOT NULL,
  `ngay_lap` datetime DEFAULT current_timestamp(),
  `id_nhan_vien` int(11) DEFAULT NULL,
  `id_khach_hang` int(11) DEFAULT NULL,
  `tong_tien` decimal(15,2) DEFAULT 0.00,
  `loai_don_hang` tinyint(1) DEFAULT 0 COMMENT '0: Tai cho, 1: Giao hang',
  `trang_thai_giao` tinyint(1) DEFAULT 0 COMMENT '0: Cho xu ly, 1: Dang giao, 2: Da giao, 3: Da huy',
  `dia_chi_giao` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `khach_hang`
--

CREATE TABLE `khach_hang` (
  `id` int(11) NOT NULL,
  `ho_ten` varchar(255) NOT NULL,
  `so_dien_thoai` varchar(15) DEFAULT NULL,
  `dia_chi` text DEFAULT NULL,
  `diem_tich_luy` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `khach_hang`
--

INSERT INTO `khach_hang` (`id`, `ho_ten`, `so_dien_thoai`, `dia_chi`, `diem_tich_luy`) VALUES
(1, 'Nguyễn Văn A', '0901234567', '123 Đường Lê Lợi, Hà Nội', 10),
(2, 'Trần Thị B', '0912345678', '456 Quận 1, TP.HCM', 5),
(3, 'Lê Văn C', '0987654321', '789 Đường Hùng Vương, Đà Nẵng', 0),
(4, 'Dương Thanh Tâm', '0352077311', 'Bắc Giang', 0);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `nhan_vien`
--

CREATE TABLE `nhan_vien` (
  `id` int(11) NOT NULL,
  `ma_nv` varchar(20) NOT NULL,
  `ho_ten` varchar(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `chuc_vu` varchar(50) DEFAULT NULL,
  `trang_thai` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `nhan_vien`
--

INSERT INTO `nhan_vien` (`id`, `ma_nv`, `ho_ten`, `username`, `password`, `chuc_vu`, `trang_thai`) VALUES
(1, 'NV001', 'Dương Tâm', 'tamadmin', '123456', 'admin', 0),
(2, 'NV002', 'Dương Thanh Tâm', 'dttam', '123456', 'nhanvien', 0),
(3, 'NV003', 'Lê Hoàng Long', 'longlh', '123456', 'nhanvien', 0),
(4, 'NV004', 'Phạm Minh Tuấn', 'tuanpm', '123456', 'nhanvien', 0),
(5, 'NV005', 'Võ Thị Mỹ Hạnh', 'hanhvtm', '123456', 'nhanvien', 0),
(6, 'NV006', 'Thân Nhung', 'nhungnv', '123456', 'nhanvien', 0);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `nhap_hang`
--

CREATE TABLE `nhap_hang` (
  `id` int(11) NOT NULL,
  `ngay_nhap` datetime DEFAULT current_timestamp(),
  `id_nhan_vien` int(11) DEFAULT NULL,
  `id_nha_cung_cap` int(11) DEFAULT NULL,
  `tong_tien_nhap` decimal(15,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `nhap_hang`
--

INSERT INTO `nhap_hang` (`id`, `ngay_nhap`, `id_nhan_vien`, `id_nha_cung_cap`, `tong_tien_nhap`) VALUES
(2, '2026-04-20 23:26:26', 2, 1, 50000.00),
(3, '2026-04-20 23:42:45', 1, 3, 100000.00);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `nha_cung_cap`
--

CREATE TABLE `nha_cung_cap` (
  `id` int(11) NOT NULL,
  `ten_ncc` varchar(255) NOT NULL,
  `so_dien_thoai` varchar(15) DEFAULT NULL,
  `dia_chi` text DEFAULT NULL,
  `ghi_chu` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `nha_cung_cap`
--

INSERT INTO `nha_cung_cap` (`id`, `ten_ncc`, `so_dien_thoai`, `dia_chi`, `ghi_chu`) VALUES
(1, 'Công ty TNHH Công nghệ Sao Mai', '0243123456', '123 Cầu Giấy, Hà Nội', 'Cung cấp linh kiện máy tính, chiết khấu 5%'),
(2, 'Tập đoàn May mặc Phong Phú', '0283888999', '456 Lê Văn Việt, TP. Thủ Đức', 'Nhà cung cấp vải sợi chính, thanh toán gối đầu'),
(3, 'Văn phòng phẩm Hồng Hà', '0243987654', '25 Lý Thường Kiệt, Hoàn Kiếm, Hà Nội', 'Cung cấp đồ dùng văn phòng, giao hàng nhanh'),
(4, 'Công ty Vận tải Thành Công', '0901234567', '789 Nguyễn Văn Linh, Quận 7, TP.HCM', 'Đối tác logistics miền Nam, hỗ trợ lưu kho'),
(5, 'Nông sản Sạch Đà Lạt', '02633555222', '10 Phan Đình Phùng, Đà Lạt, Lâm Đồng', 'Cung cấp thực phẩm sạch, đạt chuẩn VietGAP');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `san_pham`
--

CREATE TABLE `san_pham` (
  `id` int(11) NOT NULL,
  `ten_sp` varchar(255) NOT NULL,
  `id_danh_muc` int(11) DEFAULT NULL,
  `id_dvt` int(11) DEFAULT NULL,
  `gia_ban` decimal(15,2) DEFAULT NULL,
  `so_luong_ton` float DEFAULT 0,
  `ngay_nhap` date DEFAULT NULL,
  `han_su_dung` int(11) DEFAULT NULL,
  `nguon_goc` varchar(255) DEFAULT NULL,
  `hinh_anh` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `san_pham`
--

INSERT INTO `san_pham` (`id`, `ten_sp`, `id_danh_muc`, `id_dvt`, `gia_ban`, `so_luong_ton`, `ngay_nhap`, `han_su_dung`, `nguon_goc`, `hinh_anh`) VALUES
(1, 'cà chua ', NULL, NULL, 15000.00, 9, NULL, 2027, NULL, 'images/cachua.jpg'),
(2, 'Cà Chua bi', NULL, NULL, 25000.00, 103, NULL, 2027, 'Đà Lạt', 'images/cachua.jpg'),
(3, 'Rau Muống sạch', NULL, NULL, 12000.00, 50, NULL, 2026, 'Long An', 'images/raumuong.jpg'),
(4, 'Dưa Leo', NULL, NULL, 18000.00, 80, NULL, 2027, 'Tiền Giang', 'images/dualeo.jpg'),
(5, 'Cà Rốt Đà Lạt', NULL, NULL, 30000.00, 60, NULL, 2027, 'Đà Lạt', 'images/carot.jpg'),
(6, 'Súp Lơ Xanh', NULL, NULL, 35000.00, 40, NULL, 2026, 'Lâm Đồng', 'images/suplo.jpg');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `thanh_ly_huy_hang`
--

CREATE TABLE `thanh_ly_huy_hang` (
  `id` int(11) NOT NULL,
  `id_san_pham` int(11) DEFAULT NULL,
  `id_nhan_vien` int(11) DEFAULT NULL,
  `so_luong_huy` float DEFAULT NULL,
  `ngay_huy` datetime DEFAULT current_timestamp(),
  `ly_do` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `chi_tiet_hoa_don`
--
ALTER TABLE `chi_tiet_hoa_don`
  ADD PRIMARY KEY (`id_hoa_don`,`id_san_pham`),
  ADD KEY `fk_cthd_sanpham` (`id_san_pham`);

--
-- Chỉ mục cho bảng `chi_tiet_nhap_hang`
--
ALTER TABLE `chi_tiet_nhap_hang`
  ADD PRIMARY KEY (`id_nhap_hang`,`id_san_pham`),
  ADD KEY `id_san_pham` (`id_san_pham`);

--
-- Chỉ mục cho bảng `danh_muc`
--
ALTER TABLE `danh_muc`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `don_vi_tinh`
--
ALTER TABLE `don_vi_tinh`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `hoa_don`
--
ALTER TABLE `hoa_don`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_nhan_vien` (`id_nhan_vien`),
  ADD KEY `id_khach_hang` (`id_khach_hang`);

--
-- Chỉ mục cho bảng `khach_hang`
--
ALTER TABLE `khach_hang`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `so_dien_thoai` (`so_dien_thoai`);

--
-- Chỉ mục cho bảng `nhan_vien`
--
ALTER TABLE `nhan_vien`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ma_nv` (`ma_nv`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Chỉ mục cho bảng `nhap_hang`
--
ALTER TABLE `nhap_hang`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_nhan_vien` (`id_nhan_vien`),
  ADD KEY `id_nha_cung_cap` (`id_nha_cung_cap`);

--
-- Chỉ mục cho bảng `nha_cung_cap`
--
ALTER TABLE `nha_cung_cap`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `san_pham`
--
ALTER TABLE `san_pham`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_danh_muc` (`id_danh_muc`),
  ADD KEY `id_dvt` (`id_dvt`);

--
-- Chỉ mục cho bảng `thanh_ly_huy_hang`
--
ALTER TABLE `thanh_ly_huy_hang`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_san_pham` (`id_san_pham`),
  ADD KEY `id_nhan_vien` (`id_nhan_vien`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `danh_muc`
--
ALTER TABLE `danh_muc`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `don_vi_tinh`
--
ALTER TABLE `don_vi_tinh`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `hoa_don`
--
ALTER TABLE `hoa_don`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `khach_hang`
--
ALTER TABLE `khach_hang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT cho bảng `nhan_vien`
--
ALTER TABLE `nhan_vien`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `nhap_hang`
--
ALTER TABLE `nhap_hang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT cho bảng `nha_cung_cap`
--
ALTER TABLE `nha_cung_cap`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT cho bảng `san_pham`
--
ALTER TABLE `san_pham`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `thanh_ly_huy_hang`
--
ALTER TABLE `thanh_ly_huy_hang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `chi_tiet_hoa_don`
--
ALTER TABLE `chi_tiet_hoa_don`
  ADD CONSTRAINT `fk_cthd_hoadon` FOREIGN KEY (`id_hoa_don`) REFERENCES `hoa_don` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_cthd_sanpham` FOREIGN KEY (`id_san_pham`) REFERENCES `san_pham` (`id`) ON DELETE CASCADE;

--
-- Các ràng buộc cho bảng `chi_tiet_nhap_hang`
--
ALTER TABLE `chi_tiet_nhap_hang`
  ADD CONSTRAINT `chi_tiet_nhap_hang_ibfk_1` FOREIGN KEY (`id_nhap_hang`) REFERENCES `nhap_hang` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `chi_tiet_nhap_hang_ibfk_2` FOREIGN KEY (`id_san_pham`) REFERENCES `san_pham` (`id`) ON DELETE CASCADE;

--
-- Các ràng buộc cho bảng `hoa_don`
--
ALTER TABLE `hoa_don`
  ADD CONSTRAINT `hoa_don_ibfk_1` FOREIGN KEY (`id_nhan_vien`) REFERENCES `nhan_vien` (`id`),
  ADD CONSTRAINT `hoa_don_ibfk_2` FOREIGN KEY (`id_khach_hang`) REFERENCES `khach_hang` (`id`);

--
-- Các ràng buộc cho bảng `nhap_hang`
--
ALTER TABLE `nhap_hang`
  ADD CONSTRAINT `nhap_hang_ibfk_1` FOREIGN KEY (`id_nhan_vien`) REFERENCES `nhan_vien` (`id`),
  ADD CONSTRAINT `nhap_hang_ibfk_2` FOREIGN KEY (`id_nha_cung_cap`) REFERENCES `nha_cung_cap` (`id`);

--
-- Các ràng buộc cho bảng `san_pham`
--
ALTER TABLE `san_pham`
  ADD CONSTRAINT `san_pham_ibfk_1` FOREIGN KEY (`id_danh_muc`) REFERENCES `danh_muc` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `san_pham_ibfk_2` FOREIGN KEY (`id_dvt`) REFERENCES `don_vi_tinh` (`id`) ON DELETE SET NULL;

--
-- Các ràng buộc cho bảng `thanh_ly_huy_hang`
--
ALTER TABLE `thanh_ly_huy_hang`
  ADD CONSTRAINT `thanh_ly_huy_hang_ibfk_1` FOREIGN KEY (`id_san_pham`) REFERENCES `san_pham` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `thanh_ly_huy_hang_ibfk_2` FOREIGN KEY (`id_nhan_vien`) REFERENCES `nhan_vien` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
