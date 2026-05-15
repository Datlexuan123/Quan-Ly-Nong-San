-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th5 15, 2026 lúc 10:39 AM
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
  `gia_von` decimal(15,2) DEFAULT 0.00,
  `thanh_tien` decimal(15,2) GENERATED ALWAYS AS (`so_luong` * `don_gia`) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `chi_tiet_hoa_don`
--

INSERT INTO `chi_tiet_hoa_don` (`id_hoa_don`, `id_san_pham`, `so_luong`, `don_gia`, `gia_von`) VALUES
(1, 1, 3, 15000.00, 10000.00),
(2, 5, 2, 30000.00, 20000.00),
(3, 1, 1, 15000.00, 10000.00),
(3, 2, 1, 25000.00, 0.00),
(4, 3, 2, 12000.00, 0.00),
(5, 1, 1, 15000.00, 10000.00),
(6, 6, 1, 35000.00, 15000.00),
(7, 1, 1, 15000.00, 10000.00),
(8, 2, 2, 25000.00, 0.00),
(9, 3, 1, 12000.00, 0.00),
(10, 1, 1, 15000.00, 10000.00),
(11, 1, 1, 15000.00, 10000.00),
(12, 3, 1, 12000.00, 0.00),
(13, 1, 1, 15000.00, 10000.00),
(14, 2, 1, 25000.00, 0.00),
(15, 3, 1, 12000.00, 0.00),
(16, 3, 1, 12000.00, 0.00),
(17, 1, 1, 15000.00, 10000.00),
(18, 6, 1, 35000.00, 15000.00),
(19, 3, 1, 12000.00, 0.00),
(24, 2, 2, 25000.00, 13600.00),
(25, 3, 2, 15000.00, 14727.27);

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

--
-- Đang đổ dữ liệu cho bảng `chi_tiet_nhap_hang`
--

INSERT INTO `chi_tiet_nhap_hang` (`id_nhap_hang`, `id_san_pham`, `so_luong_nhap`, `gia_nhap`) VALUES
(4, 1, 20, 10000.00),
(4, 5, 10, 20000.00),
(7, 6, 2, 15000.00),
(8, 6, 2, 15000.00),
(9, 6, 2, 20000.00),
(10, 6, 2, 20000.00),
(11, 1, 5, 12.00),
(12, 2, 2, 4000.00),
(13, 1, 2, 0.00),
(14, 2, 3, 20000.00),
(15, 1, 2, 20000.00),
(16, 1, 2, 20000.00),
(17, 4, 4, 15000.00),
(18, 4, 3, 15000.00),
(19, 4, 2, 10000.00),
(20, 3, 2, 1500.00),
(21, 3, 5, 10000.00),
(22, 3, 2, 4500.00),
(23, 3, 2, 50000.00);

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

--
-- Đang đổ dữ liệu cho bảng `don_vi_tinh`
--

INSERT INTO `don_vi_tinh` (`id`, `ten_dvt`) VALUES
(1, 'Kg'),
(2, 'Bó'),
(3, 'Trái'),
(4, 'Hộp'),
(5, 'Túi');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `he_thong_log`
--

CREATE TABLE `he_thong_log` (
  `id` int(11) NOT NULL,
  `id_nhan_vien` int(11) DEFAULT NULL,
  `hanh_dong` varchar(255) DEFAULT NULL,
  `thoi_gian` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `he_thong_log`
--

INSERT INTO `he_thong_log` (`id`, `id_nhan_vien`, `hanh_dong`, `thoi_gian`) VALUES
(1, 1, 'Đã thanh toán hóa đơn #18 - Tổng: 35,000đ', '2026-05-04 11:50:38'),
(2, 2, 'Đã thanh toán hóa đơn #19 - Tổng: 12,000đ', '2026-05-04 12:05:39'),
(3, 2, 'Đã nhập phiếu hàng #11 từ NCC ID 1', '2026-05-04 12:18:50'),
(4, 2, 'Đã nhập phiếu hàng #12 từ NCC ID 1', '2026-05-04 12:19:11'),
(5, 2, 'Báo hủy SP ID:4 - SL:1.0 - Lý do: dập nát', '2026-05-04 13:34:48'),
(6, 1, 'Admin duyệt hủy SP ID:4 - SL:1.0', '2026-05-04 13:58:10'),
(7, 1, 'Admin duyệt hủy SP ID:6 - SL:2.0', '2026-05-04 14:02:32'),
(8, 1, 'Admin duyệt hủy SP ID:2 - SL:1.0', '2026-05-04 14:26:20'),
(9, 2, 'Đã thanh toán hóa đơn #20 - Tổng: 25,000đ', '2026-05-04 16:04:04'),
(10, 2, 'Đã nhập phiếu hàng #13 từ NCC ID 3', '2026-05-04 16:04:18'),
(11, 1, 'Đã thêm khách hàng mới: Nguyễn Hồng Nhung', '2026-05-04 16:05:40'),
(12, 6, 'Đã nhập phiếu hàng #14 từ NCC ID 1', '2026-05-04 16:08:36'),
(13, 2, 'Đã nhập phiếu hàng #15 từ NCC ID 1', '2026-05-09 10:08:32'),
(14, 2, 'Đã nhập phiếu hàng #16 từ NCC ID 1', '2026-05-09 10:52:17'),
(15, 2, 'Đã nhập phiếu hàng #17 từ NCC ID 1', '2026-05-09 11:24:12'),
(16, 2, 'Đã nhập phiếu hàng #18 từ NCC ID 1', '2026-05-09 12:12:44'),
(17, 2, 'Đã nhập phiếu hàng #19 từ NCC ID 1', '2026-05-09 12:20:05'),
(18, 1, 'Admin duyệt hủy SP ID:3 - SL:43.0', '2026-05-09 12:52:23'),
(19, 2, 'Đã nhập phiếu hàng #20 từ NCC ID 1', '2026-05-09 12:53:06'),
(20, 2, 'Đã nhập phiếu hàng #21 từ NCC ID 1', '2026-05-09 12:56:52'),
(21, 2, 'Đã nhập phiếu hàng #22 từ NCC ID 1', '2026-05-11 12:10:39'),
(22, 2, 'Đã thanh toán hóa đơn #23 - Tổng: 50,000đ', '2026-05-11 16:21:13'),
(23, 2, 'Đã thanh toán hóa đơn #24 - Tổng: 50,000đ', '2026-05-11 16:32:59'),
(24, 2, 'Đã nhập phiếu hàng #23 từ NCC ID 1', '2026-05-11 16:59:40'),
(25, 2, 'Đã thanh toán hóa đơn #25 - Tổng: 30,000đ', '2026-05-11 17:01:44');

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
  `dia_chi_giao` text DEFAULT NULL,
  `ghi_chu` text DEFAULT NULL,
  `phuong_thuc_thanh_toan` varchar(50) DEFAULT 'Tiền mặt'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `hoa_don`
--

INSERT INTO `hoa_don` (`id`, `ngay_lap`, `id_nhan_vien`, `id_khach_hang`, `tong_tien`, `loai_don_hang`, `trang_thai_giao`, `dia_chi_giao`, `ghi_chu`, `phuong_thuc_thanh_toan`) VALUES
(1, '2026-04-20 11:48:34', 2, 1, 45000.00, 0, 2, NULL, NULL, 'Tiền mặt'),
(2, '2026-04-21 11:48:34', 2, 4, 60000.00, 0, 2, NULL, NULL, 'Tiền mặt'),
(3, '2026-04-22 13:18:59', 1, 1, 40000.00, 0, 0, NULL, NULL, 'Tiền mặt'),
(4, '2026-04-22 13:29:00', 1, 4, 24000.00, 0, 0, NULL, NULL, 'Tiền mặt'),
(5, '2026-04-22 13:29:33', 1, 4, 14800.00, 0, 0, NULL, NULL, 'Tiền mặt'),
(6, '2026-04-22 13:30:12', 1, 4, 34900.00, 0, 1, NULL, NULL, 'Tiền mặt'),
(7, '2026-04-22 13:41:40', 1, 4, 15000.00, 0, 2, NULL, NULL, 'Tiền mặt'),
(8, '2026-04-22 13:43:28', 1, 4, 50000.00, 0, 2, NULL, NULL, 'Tiền mặt'),
(9, '2026-04-22 13:45:11', 1, 3, 12000.00, 0, 2, NULL, NULL, 'Tiền mặt'),
(10, '2026-04-22 13:51:36', 1, 6, 15000.00, 0, 2, NULL, NULL, 'Tiền mặt'),
(11, '2026-04-22 16:29:59', 1, 4, 15000.00, 0, 2, NULL, NULL, 'Tiền mặt'),
(12, '2026-04-22 17:47:15', 1, 4, 12000.00, 1, 2, 'số 2 63/56 trần quốc vươngj', 'shgdhsd', 'Tiền mặt'),
(13, '2026-04-24 17:08:48', 1, 4, 15000.00, 0, 2, 'Mua tại quầy', '', 'Chuyển khoản'),
(14, '2026-04-24 17:09:37', 1, 4, 25000.00, 1, 2, 'số100 thụy khuê', '\n[Sửa địa chỉ bởi: Dương Thanh Tâm lúc 20:51 03/05/2026]', 'Tiền mặt'),
(15, '2026-05-03 21:35:38', 1, 4, 12000.00, 1, 2, 'số 2 TQV', '', 'Tiền mặt'),
(16, '2026-05-03 22:06:12', 1, 4, 12000.00, 1, 2, 'Nhà Trọ Thuân Trà, TDP sy', '\n[Sửa địa chỉ bởi: Dương Thanh Tâm lúc 00:45 04/05/2026]', 'Tiền mặt'),
(17, '2026-05-04 00:56:06', 1, 4, 15000.00, 0, 2, 'Mua tại quầy', '', 'Tiền mặt'),
(18, '2026-05-04 11:50:38', 1, 7, 35000.00, 0, 2, 'Mua tại quầy', '', 'Tiền mặt'),
(19, '2026-05-04 12:05:39', 2, 8, 12000.00, 0, 2, 'Mua tại quầy', '', 'Tiền mặt'),
(24, '2026-05-11 16:32:59', 2, 4, 50000.00, 0, 2, 'Mua tại quầy', '', 'Tiền mặt'),
(25, '2026-05-11 17:01:44', 2, 4, 30000.00, 0, 2, 'Mua tại quầy', '', 'Tiền mặt');

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
(1, 'Nguyễn Văn A', '0901234567', '123 Đường Lê Lợi, Hà Nội', 14),
(2, 'Trần Thị B', '0912345678', '456 Quận 1, TP.HCM', 5),
(3, 'Lê Văn C', '0987654321', '789 Đường Hùng Vương, Đà Nẵng', 1),
(4, 'Dương Thanh Tâm', '0352077311', 'Bắc Giang', 12),
(5, 'Khách mới', '0352977311', NULL, 0),
(6, 'Ngọc Hà', '012344566', NULL, 1),
(7, 'Nhung Thaan', '01245678', 'Mua tại quầy', 1),
(8, 'Ngọc Hà', '0233454543', 'Mua tại quầy', 0),
(9, 'Nguyễn Thị Khanh', '0962582330', 'Mua tại quầy', 1),
(10, 'Nguyễn Hồng Nhung', '0923482334', 'HÀ Nội', 0);

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
(2, 'NV002', 'Dương Thanh Tâm', 'dttam', '12345', 'nhanvien', 0),
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
(3, '2026-04-20 23:42:45', 1, 3, 100000.00),
(4, '2026-04-19 11:48:34', 1, 5, 200000.00),
(5, '2026-04-22 15:26:03', 2, 1, 80000.00),
(6, '2026-04-22 15:26:16', 2, 1, 20000.00),
(7, '2026-04-23 13:19:55', 2, 1, 30000.00),
(8, '2026-04-23 13:20:05', 2, 1, 30000.00),
(9, '2026-04-23 13:26:34', 2, 1, 40000.00),
(10, '2026-04-23 13:27:33', 2, 1, 40000.00),
(11, '2026-05-04 12:18:50', 2, 1, 60.00),
(12, '2026-05-04 12:19:11', 2, 1, 8000.00),
(13, '2026-05-04 16:04:18', 2, 3, 0.00),
(14, '2026-05-04 16:08:36', 6, 1, 60000.00),
(15, '2026-05-09 10:08:32', 2, 1, 40000.00),
(16, '2026-05-09 10:52:17', 2, 1, 40000.00),
(17, '2026-05-09 11:24:12', 2, 1, 60000.00),
(18, '2026-05-09 12:12:44', 2, 1, 45000.00),
(19, '2026-05-09 12:20:05', 2, 1, 20000.00),
(20, '2026-05-09 12:53:06', 2, 1, 3000.00),
(21, '2026-05-09 12:56:52', 2, 1, 50000.00),
(22, '2026-05-11 12:10:39', 2, 1, 9000.00),
(23, '2026-05-11 16:59:40', 2, 1, 100000.00);

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
  `gia_nhap_gan_nhat` decimal(15,2) DEFAULT 0.00,
  `so_luong_ton` float DEFAULT 0,
  `ngay_nhap` date DEFAULT NULL,
  `han_su_dung` int(11) DEFAULT NULL,
  `nguon_goc` varchar(255) DEFAULT NULL,
  `hinh_anh` varchar(255) DEFAULT NULL,
  `trang_thai` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `san_pham`
--

INSERT INTO `san_pham` (`id`, `ten_sp`, `id_danh_muc`, `id_dvt`, `gia_ban`, `gia_nhap_gan_nhat`, `so_luong_ton`, `ngay_nhap`, `han_su_dung`, `nguon_goc`, `hinh_anh`, `trang_thai`) VALUES
(1, 'cà chua ', NULL, 1, 16000.00, 0.00, 23, NULL, 2027, NULL, 'images/cachua.jpg', 0),
(2, 'Cà Chua bi', NULL, NULL, 25000.00, 0.00, 100, NULL, 2027, 'Đà Lạt', 'images/cachua.jpg', 0),
(3, 'Rau Muống sạch', NULL, 2, 15000.00, 0.00, 9, NULL, 2026, 'Long An', 'images/raumuong.jpg', 0),
(4, 'Dưa Leo', NULL, NULL, 18000.00, 0.00, 87, NULL, 2027, 'Tiền Giang', 'images/dualeo.jpg', 0),
(5, 'Cà Rốt Đà Lạt', NULL, NULL, 30000.00, 0.00, 60, NULL, 2027, 'Đà Lạt', 'images/carot.jpg', 0),
(6, 'Súp Lơ Xanh', NULL, 1, 35000.00, 0.00, 44, NULL, 2026, 'Lâm Đồng', 'images/suplo.jpg', 0);

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
  `ly_do` varchar(255) DEFAULT NULL,
  `trang_thai` int(11) DEFAULT 0,
  `gia_tri_lo` decimal(15,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `thanh_ly_huy_hang`
--

INSERT INTO `thanh_ly_huy_hang` (`id`, `id_san_pham`, `id_nhan_vien`, `so_luong_huy`, `ngay_huy`, `ly_do`, `trang_thai`, `gia_tri_lo`) VALUES
(1, 1, 2, 1.5, '2026-04-21 11:48:34', 'Cà chua bị dập nát do vận chuyển', 0, 0.00),
(2, 6, 1, 2, '2026-04-18 11:48:34', 'Súp lơ bị héo, hết hạn sử dụng', 1, 0.00),
(3, 4, 2, 1, '2026-05-04 13:34:48', 'dập nát', 1, 0.00),
(4, 2, 2, 1, '2026-05-04 14:26:04', 'nát', 1, 0.00),
(5, 3, 1, 5, '2026-05-04 22:31:38', 'Hàng bị hỏng khi kiểm kho sáng nay', 0, 0.00),
(6, 3, 2, 43, '2026-05-09 12:51:57', 'hongr', 1, 0.00);

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
-- Chỉ mục cho bảng `he_thong_log`
--
ALTER TABLE `he_thong_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_nhan_vien` (`id_nhan_vien`);

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
  ADD KEY `fk_sanpham_dvt` (`id_dvt`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT cho bảng `he_thong_log`
--
ALTER TABLE `he_thong_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT cho bảng `hoa_don`
--
ALTER TABLE `hoa_don`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT cho bảng `khach_hang`
--
ALTER TABLE `khach_hang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT cho bảng `nhan_vien`
--
ALTER TABLE `nhan_vien`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `nhap_hang`
--
ALTER TABLE `nhap_hang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

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
-- Các ràng buộc cho bảng `he_thong_log`
--
ALTER TABLE `he_thong_log`
  ADD CONSTRAINT `he_thong_log_ibfk_1` FOREIGN KEY (`id_nhan_vien`) REFERENCES `nhan_vien` (`id`);

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
  ADD CONSTRAINT `fk_sanpham_dvt` FOREIGN KEY (`id_dvt`) REFERENCES `don_vi_tinh` (`id`) ON DELETE SET NULL,
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
