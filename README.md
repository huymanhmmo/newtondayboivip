# Website Tuyển Sinh Lớp Học Bơi Bể Bơi Newton Cầu Giấy (CanSwim)

Website được xây dựng trên nền tảng **Astro v6** (tối ưu hóa Core Web Vitals tối đa cho Local SEO) và tổ chức dữ liệu theo kiến trúc **CMS phẳng (Flat-file CMS)** bằng các file Markdown dễ dàng chỉnh sửa trực tiếp trên GitHub hoặc local IDE.

---

## 1. Hướng dẫn Quản trị Nội dung (Kiến trúc CMS phẳng)

Bạn không cần biết lập trình phức tạp để chỉnh sửa nội dung. Toàn bộ thông tin hiển thị trên website đã được bóc tách vào thư mục `src/content/`. 

Khi cần thay đổi thông tin, bạn chỉ cần mở file tương ứng trên GitHub (hoặc editor) và sửa lại phần văn bản:

- **Quản lý Khóa học & Giá học phí:** Sửa các file trong `src/content/courses/` (ví dụ: `boi-ech.md`, `boi-sai.md`,...). Bạn có thể thay đổi các trường `price_group_1` hoặc `price_group_2` trong phần frontmatter (giữa hai cặp dấu `---`).
- **Quản lý Đánh giá học viên (Testimonials):** Thêm, sửa hoặc xóa các file `.md` trong `src/content/testimonials/` để cập nhật phản hồi của phụ huynh/học viên.
- **Quản lý Câu hỏi thường gặp (FAQs):** Sửa các câu hỏi và câu trả lời trong `src/content/faqs/`.
- **Quản lý Cẩm nang bơi (Blog bài viết):** Viết bài viết mới dưới dạng file `.md` trong `src/content/blog/`. File mới sẽ tự động được hiển thị trên trang danh sách blog và sinh đường dẫn `/blog/ten-file-viet-lien-khong-dau`.

---

## 2. Hướng dẫn Chạy Local và Phát triển

### Yêu cầu hệ thống
- Cài đặt **Node.js** (Khuyến nghị phiên bản `>= 22.12.0`).

### Cài đặt và Khởi động
Di chuyển vào thư mục dự án và chạy các lệnh sau:

```bash
# Di chuyển vào thư mục website
cd E:\CLAUDE\newton.dayboi.vip\newtondayboivip

# Khởi chạy server phát triển local
npm run dev
```

Server sẽ chạy tại địa chỉ: [http://localhost:4321](http://localhost:4321). Mọi thay đổi nội dung sẽ tự động cập nhật ngay lập tức (Hot Reload).

---

## 3. Cấu hình Form đăng ký (Web3Forms)

Form đăng ký sử dụng dịch vụ **Web3Forms** (miễn phí, không cần code backend, chống spam thông minh). Để form gửi thông tin đăng ký về email `dayboivip@gmail.com` của bạn:

1. Truy cập [Web3Forms](https://web3forms.com).
2. Điền email `dayboivip@gmail.com` vào ô đăng ký để nhận **Access Key** miễn phí gửi qua email.
3. Mở file [src/components/FormRegister.astro](file:///E:/CLAUDE/newton.dayboi.vip/newtondayboivip/src/components/FormRegister.astro) và tìm dòng:
   ```typescript
   const web3formsAccessKey = "YOUR_ACCESS_KEY_HERE";
   ```
4. Thay thế bằng khóa Access Key bạn nhận được và lưu file lại.

---

## 4. Hướng dẫn Đẩy mã nguồn lên GitHub

Tất cả thay đổi đã được commit ở local. Bạn hãy mở terminal và chạy lệnh sau để đẩy code lên kho lưu trữ GitHub của bạn:

```bash
# Di chuyển vào thư mục website
cd E:\CLAUDE\newton.dayboi.vip\newtondayboivip

# Push code lên nhánh chính main
git push -u origin main
```

*(Lưu ý: Nếu GitHub yêu cầu đăng nhập, hãy sử dụng Personal Access Token hoặc xác thực thông qua trình duyệt).*

---

## 5. Hướng dẫn Deploy lên Cloudflare Pages

Sau khi đã đẩy code lên GitHub, hãy làm theo các bước sau để deploy website hoàn toàn miễn phí lên **Cloudflare Pages**:

1. Đăng nhập vào [Cloudflare Dashboard](https://dash.cloudflare.com).
2. Vào mục **Workers & Pages** ở menu bên trái -> Chọn **Create application** -> Chọn tab **Pages** -> Bấm **Connect to Git**.
3. Chọn tài khoản GitHub của bạn và chọn kho lưu trữ `newtondayboivip`.
4. Cấu hình cài đặt build (Build settings):
   - **Framework preset:** Chọn **Astro**.
   - **Build command:** `npm run build` (Mặc định).
   - **Build output directory:** `dist` (Mặc định).
   - **Root directory:** Để trống hoặc chọn thư mục chứa dự án.
5. Bấm **Save and Deploy**. Cloudflare sẽ tự động cài đặt, tối ưu hóa hình ảnh và xuất bản website của bạn chỉ trong vòng 1-2 phút.
6. Cấu hình tên miền tùy chỉnh (Custom Domain):
   - Sau khi deploy thành công, chọn tab **Custom domains** trên trang quản lý Pages dự án.
   - Bấm **Set up a custom domain** và điền tên miền `newton.dayboi.vip`.
   - Cloudflare sẽ tự động cập nhật các bản ghi DNS cần thiết để trỏ tên miền về Pages và kích hoạt HTTPS bảo mật miễn phí.

---

*Mã nguồn được cấu trúc sạch sẽ, chuẩn hóa SEO và tối ưu hóa hiệu năng tối đa bởi Antigravity AI.*
