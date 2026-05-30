---
name: canswim-seo-optimizer
description: >-
  Checklist và hướng dẫn tối ưu hóa SEO On-Page, AI Overview, và Structured Data
  (Schema JSON-LD) cho dự án CanSwim Bể bơi Newton.
---

# CanSwim SEO Optimizer Skill

## Overview
Skill này dùng để hướng dẫn các tác nhân AI và nhà phát triển tối ưu hóa SEO On-page cho hệ thống website CanSwim Bể bơi Newton (bao gồm các trang tĩnh `.astro` và bài viết cẩm nang `.md`). Trọng tâm của quy trình là tối ưu hóa hiển thị trên Google/Bing, tăng tỷ lệ trích xuất của các công cụ tìm kiếm AI (AI Overviews, Perplexity) và đảm bảo cấu trúc trang sạch sẽ, đồng bộ.

## Dependencies
- Không phụ thuộc vào script ngoài. Skill này thuộc dạng **Instruction-Only** (hướng dẫn tư duy và quy trình tối ưu).

## Quick Start
Khi nhận yêu cầu rà soát một trang hoặc viết một bài viết mới, hãy làm theo quy trình 3 bước cốt lõi:
1. **Kiểm tra kỹ thuật:** Định dạng headings (1 dòng trên desktop), kiểm tra độ dài meta title (<60 ký tự) và description (<160 ký tự).
2. **AI-Friendly Formatting:** Thêm tóm tắt TL;DR ngắn ngay sau H1, dùng bảng biểu so sánh và câu hỏi FAQ.
3. **Structured Data:** Bổ sung Schema JSON-LD (khớp 100% với text hiển thị).

---

## Workflow

### Luồng A: Rà Soát & Tối Ưu Hóa Trang Hiện Có

#### Bước 1: Rà soát Thẻ Tiêu đề & Mô tả (SEO Metadata)
- Đảm bảo thẻ `<title>` trang con có định dạng: `[Tên Trang] | CanSwim` hoặc `[Tên Trang] Bể Bơi Newton Cầu Giấy | CanSwim`. Độ dài từ **50 đến 60 ký tự**.
- Thẻ `<meta name="description">` phải tóm tắt tự nhiên nội dung trang, chứa từ khóa thực thể chính (bể bơi Newton, học bơi Cầu Giấy, học bơi Hoàng Quốc Việt) và dài từ **120 đến 155 ký tự**.
- Kiểm tra tính hợp lệ của thẻ `<link rel="canonical">` trỏ đến đúng URL tuyệt đối của trang.

#### Bước 2: Kiểm tra Quy tắc Tiêu đề 1 Dòng (Desktop)
- Mở rộng màn hình (hoặc kiểm tra file CSS [global.css](file:///e:/CLAUDE/newton.dayboi.vip/newtondayboivip/src/styles/global.css)) đảm bảo các class tiêu đề `.section-title`, `.page-title-main`, `.section-subheading`, `.commitment-title`, `.register-section-title` và các thẻ `h1`, `h2`, `h3` (trừ `.hero-title` trang chủ và tiêu đề trong `.markdown-body`) hiển thị trên **đúng 1 dòng** nhờ thuộc tính `white-space: nowrap !important;`.
- Để tránh bị khuất chữ, đảm bảo chúng sử dụng kích thước chữ co giãn linh hoạt (`clamp()`).
- Báo cáo lỗi nếu có tiêu đề bị xuống dòng hoặc tràn ngoài khung chứa một cách bất thường.

#### Bước 3: Đồng bộ hóa & Cấu trúc lại Bảng Biểu
- Đảm bảo các bảng giá học phí và vé bơi được bọc trong thẻ `<div class="canswim-table-wrapper">` và sử dụng class `<table class="canswim-table">` để hiển thị giao diện kính mờ hiện đại và đồng bộ.

#### Bước 4: Kiểm tra Structured Data (Schema JSON-LD)
- Đọc nội dung Schema JSON-LD trong code trang.
- Đối chiếu tất cả thông tin trong Schema (địa chỉ, số điện thoại, giá cả) xem có khớp 100% với nội dung text hiển thị cho người dùng không.
- Đối với trang giới thiệu địa điểm, bắt buộc có Schema `LocalBusiness` hoặc `SportsActivityLocation`.
- Đối với trang khóa học/học phí có FAQ, bắt buộc có Schema `FAQPage`.

---

### Luồng B: Định Dạng & Biên Tập Bài Viết Cẩm Nang Mới

#### Bước 1: Tối ưu cho AI Search (Chunking & TL;DR)
- Ngay phía dưới tiêu đề bài viết (H1), thêm một đoạn tóm tắt **TL;DR** (hoặc câu trả lời trực tiếp) dài từ **2 đến 4 câu (khoảng 50-80 từ)**. Đây là đoạn văn quan trọng nhất để các mô hình RAG (Truy xuất AI) chọn làm câu trả lời nhanh cho người dùng.
- Tách nội dung bài viết thành các đoạn ngắn (mỗi đoạn không quá 3-4 dòng).
- Dùng thẻ Heading (H2, H3) dạng câu hỏi thường gặp (ví dụ: `### Trẻ em bao nhiêu tuổi nên học bơi tại bể bơi Newton?`).

#### Bước 2: Chèn Bảng so sánh & Danh sách Bullets
- Bất cứ khi nào trình bày các thông tin dạng so sánh, danh sách, hãy sử dụng bảng Markdown hoặc danh sách không thứ tự (`-` hoặc `*`). AI search có xu hướng ưu tiên lấy dữ liệu từ bảng biểu và danh sách trực quan để trích dẫn.

#### Bước 3: Tối ưu hóa Thực thể (Entity) & Liên kết Nội bộ (Internal Link)
- Chèn liên kết nội bộ tự nhiên đến các trang dịch vụ cốt lõi của website theo ngữ cảnh:
  - Trỏ về [Trang chủ](file:///e:/CLAUDE/newton.dayboi.vip/newtondayboivip/src/pages/index.astro) với anchor text liên quan đến "Học bơi Cầu Giấy" hoặc "CanSwim".
  - Trỏ về [Trang giới thiệu bể bơi Newton](file:///e:/CLAUDE/newton.dayboi.vip/newtondayboivip/src/pages/be-boi-newton-hoang-quoc-viet.astro) khi nhắc tới địa điểm hoặc giá vé vào cửa.
  - Trỏ về [Trang học phí & lịch học](file:///e:/CLAUDE/newton.dayboi.vip/newtondayboivip/src/pages/lich-hoc-hoc-phi-day-boi-newton.astro) khi đề cập đến giá các khóa học bơi.

#### Bước 4: Tăng Tín Hiệu Tin Cậy (E-E-A-T)
- Đảm bảo cuối bài viết hiển thị:
  - Tên tác giả (ví dụ: *Tác giả: HLV CanSwim*).
  - Ngày cập nhật mới nhất.
  - Nguồn tham khảo chính thống (nếu có).

---

## Common Mistakes
1. **Lệch thông tin Schema:** Điền thông tin giá vé hoặc hotline trong Schema JSON-LD khác với thông tin hiển thị trên giao diện người dùng. Google có thể phạt vì hành vi spam structured data.
2. **Nhồi nhét từ khóa (Keyword Stuffing):** Cố gắng chèn từ khóa "bể bơi Newton" hay "học bơi Cầu Giấy" quá nhiều lần trong một đoạn ngắn. Hãy viết tự nhiên để người dùng đọc trước, AI đọc sau (People-first).
3. **Tiêu đề quá dài:** Viết tiêu đề quá dài trên các trang tĩnh khiến tiêu đề bị tràn viền hoặc co chữ lại quá nhỏ trên desktop. Giữ tiêu đề ngắn gọn, súc tích.
