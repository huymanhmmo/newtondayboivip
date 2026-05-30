---
name: canswim-seo-optimizer
description: >-
  Checklist, hướng dẫn và công cụ kiểm tra (seo_check.py) tối ưu hóa SEO On-Page, E-E-A-T, AI Overview, và Structured Data cho website Newton Dayboi.
---

# CanSwim SEO Optimizer Skill

## Overview
Skill này dùng để hướng dẫn các tác nhân AI và nhà phát triển tối ưu hóa SEO On-page cho hệ thống website CanSwim Bể bơi Newton (bao gồm các trang tĩnh `.astro` và bài viết cẩm nang `.md`). Trọng tâm của quy trình là tối ưu hóa hiển thị trên Google/Bing, tăng tỷ lệ trích xuất của các công cụ tìm kiếm AI (AI Overviews, Bing Copilot) năm 2026, đảm bảo tính tuân thủ E-E-A-T và cấu trúc trang sạch sẽ, đồng bộ.

Skill này tích hợp một script Python phụ trợ tại `skills/canswim-seo-optimizer/scripts/seo_check.py` để chấm điểm SEO tự động (thang 100 điểm) và đưa ra báo cáo lỗi trực quan.

## Cách Kích Hoạt Lệnh Nhanh
Để kích hoạt skill này bất kỳ lúc nào trong cuộc hội thoại, bạn chỉ cần gõ `/canswim-seo` ở đầu tin nhắn kèm theo từ khóa hoặc đường dẫn trang web cần tối ưu/viết mới. Ví dụ:
- `/canswim-seo viết bài viết mới về chủ đề: Học bơi ếch tại bể bơi Newton`
- `/canswim-seo rà soát và chấm điểm bài viết: src/content/blog/lop-hoc-boi-tre-em-cau-giay.md`

Tác nhân AI sẽ tự động đọc tài liệu này, chạy script chấm điểm `seo_check.py` và tối ưu hóa bài viết đạt điểm tuyệt đối (>95/100) theo các quy trình dưới đây.

## Dependencies
- Để chạy script phụ trợ: Yêu cầu cài đặt Python 3 và chạy bằng công cụ quản lý package `uv` thông qua lệnh: `uv run python`.

## Quick Start
Khi nhận yêu cầu viết một bài viết cẩm nang mới hoặc rà soát trang, hãy thực hiện quy trình sau:
1. **Biên tập / Tối ưu hóa**: Đảm bảo bài viết đạt độ dài 3000-5000 từ, tối thiểu 10 H2 và phân cấp H3, H4. *Chú ý*: KHÔNG chèn Mục lục ở trong nội dung bài viết vì hệ thống đã tự động hiển thị Mục lục cố định tại sidebar bên trái bài viết.
2. **Rà soát chất lượng & format**: Rà soát kỹ lưỡng để xóa bỏ tất cả các lỗi chính tả, các ký tự lạ hoặc lỗi định dạng dư thừa (như ký hiệu `**` bị hỏng, dấu ngoặc lộn xộn) do AI tạo ra. Ghi nhận tác giả **Bùi Văn Cán** kèm ảnh đại diện/bio chuyên nghiệp. Chèn tối thiểu 2 ảnh AI (từ `/images/tuyen-sinh/`) và 3 ảnh thật của bể bơi (từ `/images/` trừ `tuyen-sinh/`). Tạo liên kết nội bộ đến cả 6 trang dịch vụ chính.
3. **Chạy Script kiểm tra**: Chạy công cụ chấm điểm để quét lỗi và lấy điểm số:
   ```bash
   uv run python skills/canswim-seo-optimizer/scripts/seo_check.py check-file src/content/blog/tên-bài-viết.md
   ```
4. **Sửa lỗi & Xuất Schema**: Sửa tất cả các lỗi được báo cáo cho đến khi bài viết đạt điểm tối ưu (>95/100). Sử dụng lệnh sinh schema JSON-LD mẫu để nhúng vào trang:
   ```bash
   uv run python skills/canswim-seo-optimizer/scripts/seo_check.py generate-schema BlogPosting
   ```

---

## Quy Trình Tối Ưu Hóa Chi Tiết (Workflow)

### Luồng A: Quy Trình Viết Bài SEO Chùm (Multi-Keyword Super Pillar)
Phương pháp này giúp một bài viết duy nhất bao phủ trọn vẹn một chủ đề lớn và xếp hạng (rank) cho hàng trăm đến hàng nghìn từ khóa biến thể (long-tail, câu hỏi PAA) bằng cách xây dựng một bài viết "Siêu Pillar" sâu sắc, có cấu trúc ngữ nghĩa (Semantic SEO) vững chắc.

#### Bước 1: Lập bản đồ từ khóa ngữ nghĩa (Semantic Keyword Mapping)
- Không gom danh sách từ khóa rời rạc rồi nhồi nhét. Hãy chọn một **chủ đề chính (Head Term)** rộng (ví dụ: `Học bơi Cầu Giấy`).
- Tìm kiếm "vũ trụ" từ khóa long-tail và câu hỏi xung quanh bằng cách lấy dữ liệu từ Google Autocomplete, People Also Ask (PAA), các từ khóa liên quan ở chân trang tìm kiếm.
- Nhóm các từ khóa này theo **Ý định tìm kiếm (Search Intent)** tương ứng để chuẩn bị lên tiêu đề phụ H2/H3.

#### Bước 2: Thiết kế cấu trúc Heading dựa trên Intent của Cụm Từ Khóa
Thiết kế bài viết tối thiểu 10 thẻ H2 phân chia khoa học theo các nhóm mục tiêu:
1. **Định nghĩa & Lợi ích** (H2 dạng: *Học bơi tại bể bơi Newton có tốt không?*, *X là gì?*)
2. **Hướng dẫn Chi tiết / Cách làm** (H2 dạng: *Lộ trình học bơi ếch/bơi sải từ cơ bản đến nâng cao*)
3. **Phân loại / Gói dịch vụ** (H2 dạng: *Các khóa học bơi tiêu chuẩn tại trung tâm CanSwim*)
4. **So sánh trực quan** (H2 dạng: *So sánh lớp bơi nhóm nhỏ và lớp bơi tập thể*)
5. **Sai lầm thường gặp / Pitfalls** (H2 dạng: *Những sai lầm khiến học viên học mãi không biết bơi*)
6. **Câu hỏi thường gặp / FAQs** (H2 dạng: *Những câu hỏi thường gặp về lịch học và học phí bể bơi Newton*)

#### Bước 3: Viết Nội Dung & Tối Ưu Hóa Ngữ Nghĩa (Semantic Content Enrichment)
- **Độ dài bắt buộc**: Phải viết sâu rộng từ **3000 đến 5000 từ**.
- **Đa dạng hóa cách diễn đạt**: Sử dụng các từ đồng nghĩa và từ liên quan thuộc cùng một "neighborhood" ngữ nghĩa (ví dụ: thay vì lặp đi lặp lại "học bơi", hãy dùng "tập bơi", "rèn luyện kỹ năng dưới nước", "kỹ thuật bơi lội").
- **Tối ưu hóa hình ảnh**: Chèn tối thiểu 2 ảnh AI (thư mục `tuyen-sinh/`) và 3 ảnh thật (thư mục `images/` gốc). Đặt alt chứa từ khóa ngữ nghĩa và thêm chú thích ảnh `<p class="image-caption">`.
- **Liên kết 6 trang chính**: Chèn liên kết nội bộ tự nhiên đến toàn bộ 6 trang đích cốt lõi của website Newton Dayboi.
- **Liên kết bài viết liên quan**: Mỗi bài viết cẩm nang cần chèn tối thiểu 1 liên kết nội bộ tự nhiên trỏ đến bài viết cẩm nang liên quan khác trên website để tạo cấu trúc liên kết chéo (silo structure) giữa các bài viết.
- **E-E-A-T tác giả**: Cuối bài phải có hộp thông tin tác giả **Bùi Văn Cán** kèm hình ảnh đại diện và LinkedIn link.
- **Xóa định dạng rác của AI**: Rà soát, dọn dẹp các lỗi chính tả, các ký tự lạ hoặc lỗi định dạng dư thừa (như ký hiệu `**` bị hiển thị nguyên bản trong tiêu đề/nội dung) do lỗi của bộ sinh văn bản AI.

#### Bước 4: Tối ưu hóa liên tục dựa trên dữ liệu Google Search Console (GSC)
*Đây là chìa khóa để bài viết mở rộng từ vài chục lên hàng nghìn từ khóa sau khi xuất bản:*
1. Sau khi bài viết được xuất bản và index khoảng 1-2 tháng, truy cập **GSC → Performance → Pages → Chọn URL bài viết**.
2. Xem tab **Queries** để lọc các truy vấn có lượt hiển thị (Impressions) cao nhưng tỷ lệ nhấp (CTR) thấp hoặc vị trí trung bình đang ở trang 2-3.
3. Cập nhật và bổ sung nội dung bài viết:
   - Thêm các đoạn văn giải thích, ví dụ hoặc bổ sung các câu hỏi FAQ tương ứng trực tiếp với các truy vấn thực tế của người dùng từ GSC.
   - Điều chỉnh nhẹ Meta Title/Description để sát hơn với các từ khóa có lượng tìm kiếm thực tế lớn.
4. Lặp lại chu kỳ tối ưu này mỗi 2 tháng để liên tục mở rộng "bể" từ khóa xếp hạng.

---

### Luồng B: Rà Soát & Tối Ưu Hóa Trang Hiện Có
1. **Kiểm tra tiêu đề**: Meta Title từ **50 đến 60 ký tự**, Meta Description từ **120 đến 160 ký tự**, chứa từ khóa chính ở đầu.
2. **Quy tắc tiêu đề 1 dòng (Desktop)**: Đảm bảo các headings H1-H4 hiển thị trên duy nhất 1 dòng trên desktop bằng cách sử dụng kích thước chữ co giãn linh hoạt (`clamp()`).
3. **Structured Data**: Nhúng Schema JSON-LD (LocalBusiness, FAQPage, BlogPosting) khớp 100% với nội dung text hiển thị.
4. **Kiểm tra robots.txt**: Đảm bảo robots.txt cho phép các AI crawler (`Google-Extended`, `GPTBot`, `MicrosoftCopilot`, etc.) và trỏ đúng Sitemap.

---

## Công Cụ Kiểm Tra Tự Động (`seo_check.py`)

Hãy sử dụng script kiểm tra để tự động hóa quy trình rà soát:

### Lệnh 1: Kiểm tra một trang hoặc bài viết
```bash
uv run python skills/canswim-seo-optimizer/scripts/seo_check.py check-file [đường_dẫn_file]
```
*Ví dụ:*
```bash
uv run python skills/canswim-seo-optimizer/scripts/seo_check.py check-file src/content/blog/lop-hoc-boi-tre-em-cau-giay.md
```

### Lệnh 2: Quét hàng loạt một thư mục
```bash
uv run python skills/canswim-seo-optimizer/scripts/seo_check.py check-dir src/content/blog/
```

### Lệnh 3: Kiểm tra cấu hình robots.txt cho AI crawler
```bash
uv run python skills/canswim-seo-optimizer/scripts/seo_check.py check-robots public/robots.txt
```

### Lệnh 4: Sinh Schema JSON-LD boilerplate
```bash
uv run python skills/canswim-seo-optimizer/scripts/seo_check.py generate-schema BlogPosting
```

---

## Common Mistakes
1. **Heading bị xuống dòng (Desktop)**: Để headings quá dài (>100 ký tự) hoặc chèn thẻ ngắt dòng `<br>` khiến tiêu đề bị gãy thành 2 dòng trên desktop (Quy tắc của dự án yêu cầu tiêu đề H1-H4 hiển thị trên 1 dòng duy nhất trừ trang chủ).
2. **Thiếu liên kết trang chính**: Chỉ liên kết qua lại giữa các bài viết blog mà quên liên kết đến các trang dịch vụ đích như Trang học phí (`/lich-hoc-hoc-phi-day-boi-newton/`) hay Lớp trẻ em.
3. **Alt ảnh sơ sài**: Điền Alt ảnh trùng với tên file hoặc chỉ có 1-2 từ vô nghĩa. Alt ảnh phải là một câu đầy đủ mô tả hành động trong ảnh và chứa từ khóa thực thể.
4. **Lệch thông tin Schema**: Điền thông tin địa chỉ, hotline, hoặc tên tác giả trong JSON-LD khác với nội dung text hiển thị cho người dùng.
5. **Chặn AI Crawlers**: Đặt cấu hình chặn (`Disallow: /`) nhầm bot `Google-Extended` hay `MicrosoftCopilot` trong file `robots.txt`.
6. **Để sót ký tự rác của AI**: Để lại các dấu sao thừa thãi như `**` hoặc các lỗi chính tả, dấu câu lạ do các mô hình ngôn ngữ lớn (LLM) sinh ra.
7. **Có Mục lục trong nội dung**: Chèn phần `## Mục lục` thủ công vào bài viết gây trùng lặp với Mục lục cố định tại thanh bên trái của trang bài viết.
