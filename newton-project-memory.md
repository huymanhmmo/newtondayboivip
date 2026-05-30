# BỘ NHỚ DỰ ÁN NEWTON.DAYBOI.VIP
> Cập nhật lần cuối: 2026-05-30

## 1. THÔNG TIN DỰ ÁN

| Mục | Chi tiết |
|-----|---------|
| **Website** | newton.dayboi.vip |
| **Thương hiệu** | Trung tâm dạy bơi CanSwim |
| **Địa điểm** | Bể bơi Newton |
| **Framework** | Astro (SSG) |
| **Deploy** | Cloudflare Pages / Workers |
| **Repo** | https://github.com/huymanhmmo/newtondayboivip.git |
| **Hotline** | 0907 992 336 |
| **Email** | dayboivip@gmail.com |
| **Fanpage** | https://www.facebook.com/beboinewton |
| **GA4** | G-74CCVG5VNC |
| **Form** | Web3Forms (key: d8787c88-e215-4ba2-bed2-3510c5a2c41c) |

---

## 2. ĐỊA CHỈ CHUẨN (BẮT BUỘC DÙNG)

### Địa chỉ đầy đủ:
```
Bể bơi Newton
khu Trường Newton
lô TH2 khu đô thị Nam Cường
cuối ngõ 234 Hoàng Quốc Việt
phường Nghĩa Đô
quận Cầu Giấy
Hà Nội
```

### Biến thể SEO được phép:
- Bể bơi Newton Hoàng Quốc Việt
- Bể bơi Newton Cầu Giấy
- Bể bơi Newton Nghĩa Đô

### KHÔNG dùng:
- ❌ "khu đô thị Hoàng Quốc Việt" (SAI - phải là "khu đô thị Nam Cường")
- ❌ "Trường Tiểu học Newton" (chỉ dùng "Trường Newton" hoặc "Newton School")
- ❌ canswim.vn (domain cũ)
- ❌ "bể trong nhà" hoặc "ngoài trời"
- ✅ ĐƯỢC DÙNG: "bể bơi có mái che"

### Hướng dẫn đường đi:
1. Từ Hoàng Quốc Việt rẽ vào ngõ 234
2. Đi thẳng cuối ngõ
3. Vào khu đô thị Nam Cường
4. Trong khuôn viên trường Newton
- Dấu hiệu: Biển Trường Newton / Newton School

---

## 3. CHÍNH SÁCH KHUYẾN MẠI (QUAN TRỌNG NHẤT)

### Thông điệp chính:
> **ĐĂNG KÝ 1 KHÓA – NHẬN NGAY 30 VÉ VÀO BỂ**
> **15 BUỔI CÙNG HLV + TẶNG THÊM 15 BUỔI TỰ BƠI**

### Chi tiết áp dụng (khóa tiêu chuẩn):
- ✅ 15 buổi học với HLV
- ✅ Đã bao gồm 15 vé vào bể
- ✅ Sau khóa tặng thêm 15 buổi tự bơi
- ➡ Tổng cộng **30 lượt vào bể**

### Cam kết:
- Nếu học viên chậm → tiếp tục hỗ trợ đến khi bơi tốt

### Lưu ý:
- Không hoàn tiền
- Không sang nhượng
- Không quy đổi tiền mặt

---

## 4. CÁC GÓI KHÓA HỌC

### Khóa tiêu chuẩn (CMS: src/content/courses/):

| Khóa | Nhóm 1-3 | Nhóm 4-6 |
|------|-----------|-----------|
| Bơi Ếch | 3.000.000đ | 2.500.000đ |
| Bơi Sải | 3.500.000đ | 3.000.000đ |
| Bơi Ngửa | 3.500.000đ | 3.000.000đ |
| Bơi Bướm | 4.500.000đ | 4.000.000đ |
| COMBO Ếch + Sải | 6.000.000đ | - |

> Tất cả khóa tiêu chuẩn: 15 buổi + 15 vé bơi + tặng 15 buổi tự bơi

### GÓI MỚI - Lớp bơi tập thể:

| Mục | Chi tiết |
|-----|---------|
| **Giá** | 1.500.000đ / khóa |
| **Sĩ số** | 10 học viên / 1 HLV / 1 ca |
| **Số buổi** | 10 buổi |
| **Vé bơi** | Đã gồm 10 vé vào bể |
| **Đối tượng** | Sinh viên, nhân viên văn phòng, ≥10 tuổi |

### ⚠ LƯU Ý LỚP TẬP THỂ:
- ❌ KHÔNG tặng thêm vé bơi
- ❌ KHÔNG áp dụng dưới 10 tuổi
- ❌ KHÔNG linh động lịch
- Học theo lịch cố định của bể

---

## 5. CẤU TRÚC WEBSITE

### Pages (src/pages/):
| File | Trang |
|------|-------|
| index.astro | Landing page chính |
| be-boi-newton-hoang-quoc-viet.astro | Giới thiệu bể bơi |
| lop-hoc-boi-tre-em-be-boi-newton.astro | Lớp bơi trẻ em |
| hoc-boi-nguoi-lon-be-boi-newton.astro | Lớp bơi người lớn |
| lich-hoc-hoc-phi-day-boi-newton.astro | Lịch học & Học phí |
| lien-he-chi-duong-be-boi-newton.astro | Liên hệ & Chỉ đường |
| cam-nang/ | Blog cẩm nang bơi |

### Components (src/components/):
| File | Chức năng |
|------|----------|
| Header.astro | Header + Navigation |
| Footer.astro | Footer + NAP info |
| FormRegister.astro | Form đăng ký (Web3Forms) |
| CourseCard.astro | Card hiển thị khóa học |
| TestimonialCard.astro | Card đánh giá |
| MapEmbed.astro | Nhúng Google Maps |

### Content Collections (src/content/):
| Thư mục | Schema |
|---------|--------|
| courses/ | title, price_group_1/2, image, order |
| faqs/ | question, order (body = answer) |
| testimonials/ | name, role, avatar, stars, order |
| blog/ | title, description, pubDate, image, tags |

---

## 6. QUY TẮC NỘI DUNG

### Thuật ngữ:
- Ưu tiên dùng: **HLV** (Huấn luyện viên)
- Chấp nhận: "giáo viên", "thầy"
- Không dùng: "Trường Tiểu học Newton"

### CTA thống nhất:
- 👉 Đăng ký ngay
- 👉 Nhận tư vấn khóa phù hợp
- 👉 Giữ chỗ lớp gần nhất
- 👉 Inbox để xem lịch
- 👉 Gọi ngay 0907 992 336

### SEO Local keywords:
- CanSwim bể bơi Newton
- lớp học bơi Newton
- học bơi Hoàng Quốc Việt
- học bơi Nghĩa Đô
- lớp bơi Newton Cầu Giấy

### Tone hình ảnh/banner:
- Sáng, xanh nước, năng lượng
- Đông học viên, chuyên nghiệp
- CTA nổi
- Khuyến mại luôn nổi nhất

---

## 7. LỊCH SỬ THAY ĐỔI

### 2026-05-30 - Rà soát thống nhất nội dung
- Sửa địa chỉ Footer.astro: "khu đô thị Hoàng Quốc Việt" → "khu đô thị Nam Cường"
- Sửa địa chỉ Layout.astro Schema: "khu đô thị Hoàng Quốc Việt" → "khu đô thị Nam Cường"
- Sửa địa chỉ lien-he-chi-duong page: "khu đô thị Hoàng Quốc Việt" → "khu đô thị Nam Cường"
- Chuẩn hóa địa chỉ index.astro: thêm "khu Trường Newton, lô TH2 khu đô thị Nam Cường"
- Đổi "Giáo viên" → "HLV" trong hero section
- Thay bullet Vinhomes → "An toàn tuyệt đối trong khuôn viên trường Newton"
- Thiết lập OG images cho mạng xã hội (og-canswim-banner.jpg + og-canswim-twitter.jpg)
- Lưu bộ nhớ dự án

### 2026-05-30 - Đồng bộ theo MASTER DOCUMENT
- 🔴 Thêm banner khuyến mại "30 VÉ VÀO BỂ" nổi bật trên trang chủ (gradient, animation, glassmorphism)
- 🔴 Tạo gói Tập thể 1.500.000đ trong CMS (boi-tap-the.md)
- 🟡 Sửa CourseCard: hiển thị ưu đãi (xanh cho tiêu chuẩn, cam cho tập thể)
- 🟡 Sửa combo-ech-sai.md: desc từ "15 vé bơi kèm sát" → "1-3 học viên/HLV/Ca"
- 🟡 Sửa commitment section: "Giáo viên kèm sát" → "HLV kèm sát", thêm box "15 Vé bơi đi kèm"
- 🟡 Thêm hotline CTA strip vào 3 trang phụ (trẻ em, người lớn, giới thiệu)
- 🟡 Thiết lập ảnh chia sẻ mạng xã hội theo Banner tuyển sinh (banner-tuyen-sinh-1 và 3)
- ✅ Build thành công 10 trang, không lỗi

### 2026-05-30 - Xây dựng Thư viện ảnh tuyển sinh & SEO
- 🟢 Copy và chuẩn hóa tên file 11 ảnh AI từ `E:\CLAUDE\newton.dayboi.vip\Tuyển sinh` sang `/public/images/tuyen-sinh/`
- 🟢 Xây dựng tài liệu thư viện ảnh `thu-vien-anh.md` chứa mô tả ALT tối ưu SEO và quy tắc nhúng ảnh
- 🟢 Thay đổi ảnh bìa chính và nhúng ảnh minh họa có chú thích vào 3 bài viết cẩm nang hiện tại
- 🟢 Thêm CSS responsive cho hình ảnh và chú thích `.image-caption` trong `.markdown-body` tại `[slug].astro`
- ✅ Build thành công 10 trang, không lỗi

