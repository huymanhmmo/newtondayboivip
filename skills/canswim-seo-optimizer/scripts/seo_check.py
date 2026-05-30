#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CanSwim SEO Optimizer - Checker & Scorer Script
Tự động hóa rà soát, chấm điểm SEO (Thang điểm 100) và kiểm tra Schema JSON-LD,
đặc biệt tối ưu hóa cho AI Search (Google AI Overviews, Bing Copilot) năm 2026.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
import html.parser
import io

# Force stdout/stderr to use UTF-8 encoding to avoid Windows UnicodeEncodeError
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
except (AttributeError, io.UnsupportedOperation):
    pass

# --- THÔNG TIN CHUẨN CỦA DỰ ÁN ---
PROJECT_HOTLINE = "0907 992 336"
PROJECT_ADDRESS = (
    "Bể bơi Newton, khu Trường Newton, lô TH2 khu đô thị Nam Cường, "
    "cuối ngõ 234 Hoàng Quốc Việt, phường Nghĩa Đô, quận Cầu Giấy, Hà Nội"
)
MAIN_PAGES = [
    {"name": "Trang chủ", "path": "/"},
    {"name": "Bể bơi Newton", "path": "/be-boi-newton-hoang-quoc-viet/"},
    {"name": "Lớp bơi trẻ em", "path": "/lop-hoc-boi-tre-em-be-boi-newton/"},
    {"name": "Lớp bơi người lớn", "path": "/hoc-boi-nguoi-lon-be-boi-newton/"},
    {"name": "Lịch học & Học phí", "path": "/lich-hoc-hoc-phi-day-boi-newton/"},
    {"name": "Liên hệ & Chỉ đường", "path": "/lien-he/"}
]

# --- PARSER CHO FILE ASTRO / HTML ---
class AstroHtmlParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []  # list of (tag, text)
        self.links = []     # list of href
        self.images = []    # list of (src, alt)
        self.schemas = []   # list of raw json strings
        self.text_tokens = []
        self.current_heading_tag = None
        self.current_heading_text = ""
        self.in_script_ldjson = False
        self.current_script_content = ""
        self.in_style_or_script = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_heading_tag = tag
            self.current_heading_text = ""
        elif tag == 'a' and 'href' in attr_dict:
            self.links.append(attr_dict['href'])
        elif tag == 'img':
            src = attr_dict.get('src', '')
            alt = attr_dict.get('alt', '')
            self.images.append((src, alt))
        elif tag == 'script' and attr_dict.get('type') == 'application/ld+json':
            self.in_script_ldjson = True
            self.current_script_content = ""
        elif tag in ['script', 'style']:
            self.in_style_or_script = True

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if self.current_heading_tag:
                self.headings.append((self.current_heading_tag, self.current_heading_text.strip()))
                self.current_heading_tag = None
        elif tag == 'script' and self.in_script_ldjson:
            self.schemas.append(self.current_script_content)
            self.in_script_ldjson = False
        elif tag in ['script', 'style']:
            self.in_style_or_script = False

    def handle_data(self, data):
        if self.in_script_ldjson:
            self.current_script_content += data
            return
        
        if self.current_heading_tag:
            self.current_heading_text += data
        
        if not self.in_style_or_script:
            words = [w for w in data.split() if w.strip()]
            self.text_tokens.extend(words)

# --- TRÌNH PHÂN TÍCH FRONTMATTER (DÀNH CHO FILE MD) ---
def parse_frontmatter(content):
    frontmatter = {}
    lines = content.splitlines()
    if not lines or lines[0].strip() != '---':
        return frontmatter, content
    
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_idx = i
            break
            
    if end_idx == -1:
        return frontmatter, content
        
    fm_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx+1:])
    
    for line in fm_lines:
        match = re.match(r'^([a-zA-Z0-9_-]+)\s*:\s*(.*)$', line)
        if match:
            key = match.group(1).strip()
            val = match.group(2).strip()
            # Loại bỏ dấu nháy đơn/kép ngoài cùng
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            # Xử lý mảng đơn giản [a, b, c]
            if val.startswith('[') and val.endswith(']'):
                val = [item.strip().strip('"').strip("'") for item in val[1:-1].split(',')]
            frontmatter[key] = val
            
    return frontmatter, body

# --- HÀM TÌM KIẾM HÌNH ẢNH TRONG MARKDOWN ---
def extract_md_images(body):
    # Tìm kiếm các mẫu: ![Alt](Path)
    md_image_pattern = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(md_image_pattern, body)
    images = []
    for alt, src in matches:
        images.append((src.strip(), alt.strip()))
    
    # Tìm kiếm thẻ <img> trong Markdown
    html_img_pattern = r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\']'
    html_matches = re.findall(html_img_pattern, body)
    for src, alt in html_matches:
        images.append((src.strip(), alt.strip()))
        
    return images

# --- HÀM TÌM KIẾM LIÊN KẾT TRONG MARKDOWN ---
def extract_md_links(body):
    # Tìm kiếm: [Text](Href)
    md_link_pattern = r'\[.*?\]\((.*?)\)'
    matches = re.findall(md_link_pattern, body)
    
    # Tìm kiếm thẻ <a>
    html_link_pattern = r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>'
    html_matches = re.findall(html_link_pattern, body)
    
    return [m.strip() for m in matches + html_matches]

# --- HÀM TÌM KIẾM HEADING TRONG MARKDOWN ---
def extract_md_headings(body):
    # Tìm kiếm dòng bắt đầu bằng #, ##, ###, ####
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    for line in body.splitlines():
        match = re.match(heading_pattern, line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((f"h{level}", text))
    return headings

# --- CHƯƠNG TRÌNH KIỂM TRA CHÍNH ---
def check_file(file_path, keyword=None):
    path = Path(file_path)
    if not path.exists():
        print(f"Lỗi: Không tìm thấy file {file_path}", file=sys.stderr)
        return None
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    is_md = path.suffix.lower() == '.md'
    is_astro = path.suffix.lower() == '.astro'

    # Khai báo các biến lưu trữ thông tin phân tích
    title = ""
    description = ""
    canonical = ""
    headings = []
    links = []
    images = []
    schemas = []
    body_text = ""
    word_count = 0
    has_toc = False
    author_name = ""
    has_author_avatar = False
    has_author_bio = False
    has_author_link = False
    
    report_items = []
    scores = {
        "keyword": 0,       # Max 15
        "depth": 0,         # Max 15
        "eeat": 0,          # Max 15
        "structure": 0,     # Max 15
        "readability": 0,   # Max 15
        "images": 0,        # Max 15
        "links": 0          # Max 10
    }
    
    # Mặc định từ khóa nếu không truyền
    if not keyword:
        keyword = "bể bơi newton"

    # --- PHÂN TÍCH THEO PHÂN LOẠI FILE ---
    if is_md:
        frontmatter, body = parse_frontmatter(content)
        title = frontmatter.get('title', '')
        description = frontmatter.get('description', '')
        canonical = frontmatter.get('canonical', '')
        
        # Heading từ Markdown
        headings = extract_md_headings(body)
        # Nếu có title trong frontmatter thì coi như đã có H1
        if title:
            headings.insert(0, ('h1', title))
            
        links = extract_md_links(body)
        images = extract_md_images(body)
        
        # Word count & Body
        # Lọc sạch mã markdown để đếm từ chuẩn
        clean_body = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
        clean_body = re.sub(r'!\[.*?\]\(.*?\)', '', clean_body)
        clean_body = re.sub(r'\[.*?\]\(.*?\)', '', clean_body)
        clean_body = re.sub(r'<[^>]+>', '', clean_body)
        body_text = clean_body
        word_count = len([w for w in clean_body.split() if w.strip()])
        
        # Kiểm tra Mục lục (ToC)
        has_toc = any(h[1].lower() in ['mục lục', 'table of contents', 'danh mục'] for h in headings) or "## mục lục" in body.lower()
        

        # Kiểm tra khối tác giả E-E-A-T (Bùi Văn Cán)
        author_name_match = re.search(r'tác giả\s*:\s*(bùi văn cán)', body.lower()) or "bùi văn cán" in body.lower()
        if author_name_match:
            author_name = "Bùi Văn Cán"
            
        has_author_avatar = "/images/thay-bui-van-can-canswim.jpg" in body or "avatar" in body.lower()
        has_author_bio = any(k in body.lower() for k in ["huấn luyện viên", "hlv", "kinh nghiệm", "sáng lập", "chuyên môn"])
        has_author_link = "linkedin.com" in body or "facebook.com" in body
        
        # Trích xuất Schema trong MD nếu có (thường MD ít có schema trực tiếp, nhưng kiểm tra đề phòng)
        schema_matches = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', content, flags=re.DOTALL)
        schemas = [s.strip() for s in schema_matches]
        
    elif is_astro:
        parser = AstroHtmlParser()
        parser.feed(content)
        
        headings = parser.headings
        links = parser.links
        images = parser.images
        schemas = parser.schemas
        word_count = len(parser.text_tokens)
        body_text = " ".join(parser.text_tokens)
        
        # Tìm title, meta và canonical trong code bằng Regex (Astro có thể dùng biến hoặc truyền props)
        title_match = re.search(r'<title>(.*?)</title>', content, flags=re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title_prop = re.search(r'title\s*=\s*["\']([^"\']+)["\']', content)
            title = title_prop.group(1).strip() if title_prop else ""
            
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, flags=re.DOTALL)
        if not desc_match:
            desc_match = re.search(r'content=["\'](.*?)["\']\s+name=["\']description["\']', content, flags=re.DOTALL)
        
        if desc_match:
            description = desc_match.group(1).strip()
        else:
            desc_prop = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content, flags=re.DOTALL)
            description = desc_prop.group(1).strip() if desc_prop else ""
            
        canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', content)
        if canonical_match:
            canonical = canonical_match.group(1).strip()
        else:
            canonical_prop = re.search(r'canonicalURL\s*=\s*["\']([^"\']+)["\']', content)
            canonical = canonical_prop.group(1).strip() if canonical_prop else ""
        
        # Đối với Astro tĩnh, không kiểm tra ToC, E-E-A-T khắt khe như Blog
        has_toc = True
        author_name = "Bùi Văn Cán"
        has_author_avatar = True
        has_author_bio = True
        has_author_link = True

    # ==================== 1. TỪ KHÓA & SEARCH INTENT (Max 15) ====================
    keyword_lower = keyword.lower()
    title_lower = title.lower()
    desc_lower = description.lower()
    body_lower = body_text.lower()
    
    kw_in_title = keyword_lower in title_lower
    kw_in_desc = keyword_lower in desc_lower
    
    # Tính tần suất từ khóa
    kw_count = len(re.findall(re.escape(keyword_lower), body_lower))
    kw_density = (kw_count / max(1, word_count)) * 100
    
    if kw_in_title:
        scores["keyword"] += 5
    else:
        report_items.append("[❌] **Từ khóa chính**: Không tìm thấy từ khóa '" + keyword + "' trong Meta Title.")
        
    if kw_in_desc:
        scores["keyword"] += 5
    else:
        report_items.append("[❌] **Từ khóa chính**: Không tìm thấy từ khóa '" + keyword + "' trong Meta Description.")
        
    if is_md:
        # Đối với bài viết dài 3000-5000 từ, tần suất cần xuất hiện tối thiểu 5 lần
        if kw_count >= 5:
            scores["keyword"] += 5
        else:
            report_items.append(f"[⚠️] **Mật độ từ khóa**: Từ khóa '{keyword}' chỉ xuất hiện {kw_count} lần trong nội dung (Quá ít).")
    else:
        # Đối với trang tĩnh
        if kw_count >= 2:
            scores["keyword"] += 5
        else:
            scores["keyword"] += 3

    # ==================== 2. CHẤT LƯỢNG & ĐỘ SÂU (Max 15) ====================
    if is_md:
        if 3000 <= word_count <= 5000:
            scores["depth"] += 15
        elif 1500 <= word_count < 3000:
            scores["depth"] += 10
            report_items.append(f"[⚠️] **Độ dài bài viết**: Bài viết dài {word_count} từ. Hãy bổ sung thêm nội dung chuyên sâu để đạt 3000 - 5000 từ.")
        else:
            scores["depth"] += 5
            report_items.append(f"[❌] **Độ dài bài viết**: Bài viết quá ngắn ({word_count} từ). Tiêu chuẩn 2026 yêu cầu 3000-5000 từ để phủ hết chủ đề.")
    else:
        if word_count >= 400:
            scores["depth"] += 15
        elif 200 <= word_count < 400:
            scores["depth"] += 10
        else:
            scores["depth"] += 5
            report_items.append(f"[⚠️] **Nội dung mỏng**: Trang tĩnh này chỉ có {word_count} từ. Hãy bổ sung text mô tả để tránh lỗi thin content.")

    # ==================== 3. E-E-A-T & ĐỘ TIN CẬY (Max 15) ====================
    if author_name == "Bùi Văn Cán":
        scores["eeat"] += 5
    else:
        report_items.append("[❌] **Tác giả (E-E-A-T)**: Không tìm thấy thông tin tác giả 'Bùi Văn Cán'. Tất cả bài viết phải ghi rõ tác giả.")
        
    if has_author_avatar:
        scores["eeat"] += 3
    else:
        report_items.append("[❌] **Ảnh tác giả**: Thiếu ảnh đại diện tác giả (HLV Bùi Văn Cán) ở cuối bài.")
        
    if has_author_bio:
        scores["eeat"] += 3
    else:
        report_items.append("[⚠️] **Tiểu sử tác giả**: Thiếu mô tả kinh nghiệm/chứng chỉ của tác giả để chứng minh chuyên môn.")
        
    # Kiểm tra liên kết nguồn ngoài (External links) uy tín hoặc link MXH
    external_links = [l for l in links if l.startswith('http') and 'newton.dayboi.vip' not in l]
    if len(external_links) >= 1:
        scores["eeat"] += 4
    else:
        report_items.append("[⚠️] **Trích dẫn nguồn**: Không tìm thấy liên kết ngoài (external link) trỏ đến nguồn uy tín hoặc trang LinkedIn/Facebook tác giả.")

    # ==================== 4. ON-PAGE & CẤU TRÚC KỸ THUẬT (Max 15) ====================
    # A. Kiểm tra H1
    h1_count = len([h for h in headings if h[0] == 'h1'])
    if h1_count == 1:
        scores["structure"] += 3
    elif h1_count > 1:
        report_items.append(f"[❌] **Thẻ H1**: Có {h1_count} thẻ H1 trên trang. Google chỉ khuyến nghị duy nhất 1 thẻ H1.")
    else:
        report_items.append("[❌] **Thẻ H1**: Trang này không có thẻ H1 nào.")
        
    # B. Kiểm tra H2
    h2_count = len([h for h in headings if h[0] == 'h2'])
    if is_md:
        if h2_count >= 10:
            scores["structure"] += 5
        else:
            scores["structure"] += max(1, int(h2_count * 0.5))
            report_items.append(f"[❌] **Thẻ H2**: Bài viết chỉ có {h2_count} thẻ H2 (Tiêu chuẩn yêu cầu tối thiểu 10 thẻ H2 cho bài viết dài).")
    else:
        if h2_count >= 3:
            scores["structure"] += 5
        else:
            scores["structure"] += 3
            
    # C. Kiểm tra H3 & H4
    has_h3 = any(h[0] == 'h3' for h in headings)
    has_h4 = any(h[0] == 'h4' for h in headings)
    if has_h3 and has_h4:
        scores["structure"] += 4
    elif has_h3:
        scores["structure"] += 2
        report_items.append("[⚠️] **Cấu trúc Heading**: Bài viết có H3 nhưng thiếu H4 để phân cấp sâu hơn.")
    else:
        report_items.append("[❌] **Cấu trúc Heading**: Thiếu cấu trúc phân cấp H3, H4 để phục vụ AI chunking.")
        
    # D. Kiểm tra quy tắc xuống dòng headings
    long_or_br_headings = []
    for tag, text in headings:
        if '<br>' in text.lower() or len(text) > 100:
            long_or_br_headings.append(text)
            
    if not long_or_br_headings:
        scores["structure"] += 3
    else:
        scores["structure"] += 1
        report_items.append("[❌] **Quy tắc Tiêu đề**: Phát hiện tiêu đề quá dài (>100 ký tự) hoặc chứa thẻ ngắt dòng `<br>`: " + f"'{long_or_br_headings[0][:40]}...'")

    # ==================== 5. ĐOẠN VĂN & READABILITY (Max 15) ====================
    # A. Kiểm tra Mục lục (ToC)
    if is_md:
        if has_toc:
            report_items.append("[❌] **Mục lục**: Phát hiện phần Mục lục tự viết trong nội dung bài viết. Hãy xóa đi để tránh trùng lặp với Mục lục cố định ở sidebar bên trái.")
            scores["readability"] += 2
        else:
            scores["readability"] += 5
    else:
        scores["readability"] += 5
            
    # B. Kiểm tra cấu trúc đoạn văn ngắn (đoạn dài > 5 dòng dễ gây ngán trên mobile)
    paragraphs = [p.strip() for p in body_text.split('\n\n') if p.strip()]
    long_paragraphs = 0
    for p in paragraphs:
        lines_count = len(p.split('\n'))
        # Đánh giá thô: nếu đoạn không có xuống dòng nhưng cực dài (>400 ký tự)
        if len(p) > 350 and lines_count == 1:
            long_paragraphs += 1
        elif lines_count > 4:
            long_paragraphs += 1
            
    if long_paragraphs == 0:
        scores["readability"] += 5
    elif long_paragraphs <= 3:
        scores["readability"] += 3
        report_items.append(f"[⚠️] **Trải nghiệm đọc**: Có {long_paragraphs} đoạn văn hơi dài. Hãy tách nhỏ thành 2-4 câu/đoạn.")
    else:
        report_items.append(f"[❌] **Bức tường chữ**: Phát hiện {long_paragraphs} đoạn văn quá dài. Cần tối ưu để thân thiện với mobile.")
        
    # C. Kiểm tra sự hiện diện của list/table
    has_list = "-" in body_text or "*" in body_text or "1." in body_text
    has_table = "|" in body_text or "<table" in content.lower()
    if has_list or has_table:
        scores["readability"] += 5
    else:
        report_items.append("[⚠️] **Định dạng**: Hãy thêm bảng biểu so sánh hoặc danh sách liệt kê để AI dễ trích xuất dữ liệu.")

    # D. Kiểm tra ký tự lạ và lỗi định dạng AI (như ** trong tiêu đề, dấu sao không đóng)
    bad_markdown_symbols = []
    for tag, text in headings:
        if '**' in text:
            bad_markdown_symbols.append(f"Chứa dấu sao '**' trong tiêu đề: '{text}'")
            
    asterisk_count = body_text.count('**')
    if asterisk_count % 2 != 0:
        bad_markdown_symbols.append("Phát hiện dấu '**' không có cặp đóng/mở khớp nhau trong nội dung.")
        
    # Tìm kiếm các từ bị lặp kép bất thường (chỉ trên cùng một dòng)
    double_words = re.findall(r'\b(\w+)[ \t]+\1\b', body_text.lower())
    vietnamese_valid_reduplications = {
        "xa", "nho", "đều", "sát", "to", "nhỏ", "dần", "ít", "nhiều", "sâu", "rất", "luôn", "ngày", "đêm",
        "song", "thông", "chậm", "nhanh", "dễ", "khó", "zalo", "bơi", "học"
    }
    bad_repeats = [w for w in double_words if w not in vietnamese_valid_reduplications]
    if bad_repeats:
        bad_markdown_symbols.append(f"Phát hiện từ bị lặp kép nghi ngờ lỗi chính tả: '{bad_repeats[0]} {bad_repeats[0]}'")
        
    if bad_markdown_symbols:
        scores["readability"] = max(0, scores["readability"] - 2)
        for issue in bad_markdown_symbols:
            report_items.append(f"[❌] **Ký tự rác & Lỗi AI**: {issue}")

    # ==================== 6. HÌNH ẢNH SEO (Max 15) ====================
    if not images:
        report_items.append("[❌] **Hình ảnh**: Trang này không có hình ảnh nào.")
    else:
        # A. Kiểm tra Alt text
        missing_alt = [src for src, alt in images if not alt.strip()]
        if not missing_alt:
            scores["images"] += 5
        else:
            scores["images"] += max(0, 5 - len(missing_alt))
            report_items.append(f"[❌] **Thẻ Alt**: Phát hiện {len(missing_alt)} hình ảnh thiếu mô tả Alt text.")
            
        # B. Kiểm tra tên file ảnh chuẩn SEO
        bad_filenames = []
        for src, alt in images:
            filename = src.split('/')[-1]
            # Cho phép bỏ qua tham số nếu có url query
            filename_clean = filename.split('?')[0]
            if re.search(r'[^a-z0-9\.\-_]', filename_clean) or " " in filename_clean:
                bad_filenames.append(filename)
                
        if not bad_filenames:
            scores["images"] += 3
        else:
            report_items.append(f"[⚠️] **Tên file ảnh**: File ảnh '{bad_filenames[0]}' chưa được tối ưu (chứa chữ hoa, khoảng trắng hoặc ký tự lạ).")
            
        # C. Kiểm tra Caption hình ảnh (<p class="image-caption">)
        # Chỉ check với MD, bỏ qua ảnh avatar tác giả
        if is_md:
            body_images_needing_caption = [
                (src, alt) for src, alt in images 
                if "avatar" not in src.lower() and "avatar" not in alt.lower() and "tác giả" not in alt.lower() and "thay-bui-van-can" not in src.lower()
            ]
            caption_matches = len(re.findall(r'<p\s+class=["\']image-caption["\']>', body))
            if caption_matches >= len(body_images_needing_caption):
                scores["images"] += 3
            else:
                report_items.append(f"[⚠️] **Chú thích ảnh**: Chỉ có {caption_matches}/{len(body_images_needing_caption)} ảnh có chú thích `<p class='image-caption'>` đi kèm.")
        else:
            scores["images"] += 3
            
        # D. Kiểm tra tỷ lệ ảnh AI & ảnh thật (Dành riêng cho Blog)
        if is_md:
            ai_images_count = len([src for src, alt in images if "/images/tuyen-sinh/" in src])
            real_images_count = len([src for src, alt in images if "/images/" in src and "/images/tuyen-sinh/" not in src and "avatar" not in src])
            
            ai_score = 0
            real_score = 0
            
            if ai_images_count >= 2:
                ai_score = 2
            else:
                report_items.append(f"[❌] **Ảnh AI thiết kế**: Có {ai_images_count}/2 ảnh AI tuyển sinh. Vui lòng bổ sung thêm ảnh từ thư mục `/images/tuyen-sinh/`.")
                
            if real_images_count >= 3:
                real_score = 2
            else:
                report_items.append(f"[❌] **Ảnh bể bơi thật**: Có {real_images_count}/3 ảnh chụp thực tế bể bơi. Vui lòng bổ sung thêm từ thư mục `/images/` (trừ `tuyen-sinh`).")
                
            scores["images"] += (ai_score + real_score)
        else:
            scores["images"] += 4

    # ==================== 7. LIÊN KẾT NỘI BỘ (Max 10) ====================
    # Chuẩn hóa links để so sánh dễ
    normalized_links = []
    for l in links:
        # Lấy phần path
        path_only = l.replace("https://newton.dayboi.vip", "").split('?')[0]
        # Thêm slash cuối nếu thiếu
        if not path_only.endswith('/') and '.' not in path_only.split('/')[-1]:
            path_only += '/'
        normalized_links.append(path_only)
        
    if is_md:
        found_main_pages = 0
        missing_pages = []
        for page in MAIN_PAGES:
            target_path = page["path"]
            if target_path in normalized_links:
                found_main_pages += 1
            else:
                missing_pages.append(page["name"])
                
        # Tính điểm dựa trên số lượng link chính tìm thấy
        if found_main_pages == 6:
            scores["links"] += 10
        elif 4 <= found_main_pages <= 5:
            scores["links"] += 7
            report_items.append(f"[⚠️] **Liên kết nội bộ**: Thiếu liên kết tới trang chính: {', '.join(missing_pages)}")
        elif 2 <= found_main_pages <= 3:
            scores["links"] += 4
            report_items.append(f"[❌] **Thiếu liên kết**: Thiếu liên kết tới các trang chính: {', '.join(missing_pages)}")
        else:
            scores["links"] += 1
            report_items.append(f"[❌] **Cực kỳ thiếu liên kết**: Hầu như không liên kết đến trang chính nào của website.")

        # Kiểm tra liên kết đến bài viết blog liên quan khác (silo link)
        related_blog_links = 0
        for l in normalized_links:
            is_blog_path = l.startswith('/cam-nang/') or l.startswith('/blog/')
            is_listing_page = l in ['/cam-nang/', '/blog/']
            is_self = canonical and (canonical in l or l in canonical)
            if is_blog_path and not is_listing_page and not is_self:
                related_blog_links += 1
                
        if related_blog_links >= 1:
            pass
        else:
            scores["links"] = max(0, scores["links"] - 2)
            report_items.append("[❌] **Liên kết bài viết liên quan**: Không tìm thấy liên kết nội bộ nào trỏ tới bài viết cẩm nang khác (silo link). Mỗi bài viết cẩm nang cần liên kết chéo tới ít nhất 1 bài viết cẩm nang liên quan khác.")
    else:
        # Đối với Astro trang tĩnh, chỉ cần có link sang ít nhất 2 trang chính khác
        links_to_other_main = 0
        for page in MAIN_PAGES:
            if page["path"] in normalized_links and page["path"] != canonical:
                links_to_other_main += 1
        if links_to_other_main >= 2:
            scores["links"] += 10
        else:
            scores["links"] += 5

    # ==================== PHẦN MỞ RỘNG: VALIDATE SCHEMA JSON-LD ====================
    schema_report = []
    has_valid_schema = False
    
    if schemas:
        for idx, schema_str in enumerate(schemas):
            try:
                schema_json = json.loads(schema_str)
                has_valid_schema = True
                
                # Kiểm tra thông tin NAP trong LocalBusiness / SportsActivityLocation
                stype = schema_json.get('@type', '')
                if isinstance(stype, list):
                    is_local_business = any(t in ['LocalBusiness', 'SportsActivityLocation', 'SportsClub'] for t in stype)
                else:
                    is_local_business = stype in ['LocalBusiness', 'SportsActivityLocation', 'SportsClub']
                    
                if is_local_business:
                    phone = schema_json.get('telephone', '')
                    address_obj = schema_json.get('address', {})
                    address_str = ""
                    if isinstance(address_obj, dict):
                        address_str = address_obj.get('streetAddress', '') + ", " + address_obj.get('addressLocality', '')
                    elif isinstance(address_obj, str):
                        address_str = address_obj
                        
                    # So khớp hotline
                    phone_clean = re.sub(r'\s+', '', phone)
                    target_phone_clean = re.sub(r'\s+', '', PROJECT_HOTLINE)
                    if phone_clean != target_phone_clean:
                        schema_report.append(f"[⚠️] **Schema LocalBusiness**: Hotline trong Schema '{phone}' khác hotline chuẩn '{PROJECT_HOTLINE}'.")
                        
                    # So khớp địa chỉ (so sánh tương đối một vài từ khóa cốt lõi)
                    if "nam cường" not in address_str.lower() or "nghĩa đô" not in address_str.lower():
                        schema_report.append("[⚠️] **Schema LocalBusiness**: Địa chỉ trong Schema chưa khớp chuẩn (phải chứa 'khu đô thị Nam Cường, Nghĩa Đô').")
                
                # Kiểm tra Schema Person (Bùi Văn Cán) cho Blog
                if is_md and schema_json.get('@type') in ['BlogPosting', 'Article']:
                    author_obj = schema_json.get('author', {})
                    author_name_schema = ""
                    if isinstance(author_obj, dict):
                        author_name_schema = author_obj.get('name', '')
                    elif isinstance(author_obj, list) and len(author_obj) > 0:
                        author_name_schema = author_obj[0].get('name', '') if isinstance(author_obj[0], dict) else ""
                        
                    if author_name_schema != "Bùi Văn Cán":
                        schema_report.append(f"[⚠️] **Schema BlogPosting**: Tên tác giả trong Schema '{author_name_schema}' không phải là 'Bùi Văn Cán'.")
                        
            except json.JSONDecodeError:
                schema_report.append(f"[❌] **Cú pháp Schema**: Khối JSON-LD thứ {idx+1} bị lỗi cú pháp JSON không hợp lệ.")
    else:
        # Đối với Astro, kiểm tra nếu sử dụng Layout và truyền schemaType
        layout_schema_match = False
        if is_astro:
            schema_type_match = re.search(r'schemaType\s*=\s*["\']([^"\']+)["\']', content)
            if schema_type_match:
                has_valid_schema = True
                layout_schema_match = True
        
        if not is_md and not layout_schema_match:
            # Trang tĩnh bắt buộc phải có schema
            schema_report.append("[❌] **Thiếu Structured Data**: Trang này không có thẻ Schema JSON-LD nào.")
            
    # Tính điểm thưởng/trừ dựa trên Schema
    schema_bonus = 0
    if schemas and not schema_report:
        schema_bonus = 2  # Thưởng 2 điểm nếu schema hoàn hảo
    elif schema_report:
        # Bị trừ điểm nếu schema lỗi
        scores["structure"] = max(0, scores["structure"] - 2)

    # --- TỔNG HỢP KẾT QUẢ ---
    total_score = sum(scores.values()) + schema_bonus
    total_score = min(100, total_score)  # Giới hạn max 100
    
    # Tạo output báo cáo Markdown
    report = []
    report.append(f"# BÁO CÁO KIỂM TRA SEO: {path.name}")
    report.append(f"- **Đường dẫn**: `{file_path}`")
    report.append(f"- **Từ khóa kiểm tra**: `{keyword}`")
    report.append(f"- **Độ dài bài viết**: `{word_count} từ` ({'Đạt tiêu chuẩn 3000-5000 từ' if 3000 <= word_count <= 5000 else 'Chưa đạt 3000 từ'})")
    report.append(f"- **Tổng điểm SEO**: **{total_score}/100**\n")
    
    report.append("## Điểm số chi tiết các mục:")
    for cat, val in scores.items():
        cat_name = {
            "keyword": "1. Từ khóa & Search Intent",
            "depth": "2. Chất lượng & Độ sâu",
            "eeat": "3. E-E-A-T & Tác giả Bùi Văn Cán",
            "structure": "4. On-page & Cấu trúc kỹ thuật",
            "readability": "5. Độ dễ đọc & Format",
            "images": "6. Hình ảnh SEO (AI vs Thật)",
            "links": "7. Liên kết nội bộ (6 trang chính)"
        }.get(cat, cat)
        max_val = 10 if cat == "links" else 15
        report.append(f"- **{cat_name}**: `{val}/{max_val} điểm`")
    if schema_bonus > 0:
        report.append(f"- **Điểm thưởng Structured Data (Schema)**: `+{schema_bonus} điểm`")
    report.append("")
    
    if schema_report:
        report.append("## Lỗi Structured Data (Schema JSON-LD):")
        for err in schema_report:
            report.append(err)
        report.append("")

    report.append("## Khuyến nghị và Việc cần sửa:")
    if not report_items and not schema_report and total_score >= 95:
        report.append("[✅] Tuyệt vời! Trang này đã tối ưu SEO xuất sắc, đạt tiêu chuẩn khắt khe nhất của năm 2026.")
    else:
        for item in report_items:
            report.append(item)
            
    return {
        "file": file_path,
        "score": total_score,
        "word_count": word_count,
        "report": "\n".join(report)
    }

# --- LỆNH KIỂM TRA FILE ROBOTS.TXT ---
def check_robots(robots_path):
    path = Path(robots_path)
    if not path.exists():
        return "[❌] **Không tìm thấy file robots.txt** tại đường dẫn chỉ định."
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = [l.strip().lower() for l in content.splitlines() if l.strip()]
    
    ai_bots = ['gptbot', 'chatgpt-user', 'google-extended', 'microsoftcopilot', 'perplexitybot']
    blocked_bots = []
    
    # Kiểm tra xem có bot nào bị Disallow: / không
    current_agent = None
    agent_disallows = {}
    
    for line in lines:
        if line.startswith('user-agent:'):
            current_agent = line.split(':', 1)[1].strip()
            if current_agent not in agent_disallows:
                agent_disallows[current_agent] = []
        elif line.startswith('disallow:') and current_agent:
            disallow_path = line.split(':', 1)[1].strip()
            agent_disallows[current_agent].append(disallow_path)
            
    # Phân tích xem các AI bot có bị chặn toàn diện không
    for bot in ai_bots:
        # Check khớp trực tiếp
        is_blocked = False
        for agent, disallows in agent_disallows.items():
            if bot in agent or (agent == '*' and '/' in disallows):
                if '/' in disallows or '/*' in disallows:
                    is_blocked = True
        if is_blocked:
            blocked_bots.append(bot)
            
    report = []
    report.append(f"# BÁO CÁO KIỂM TRA ROBOTS.TXT: {path.name}")
    
    if blocked_bots:
        report.append(f"[❌] **AI Crawlers bị chặn**: Phát hiện robots.txt đang chặn truy cập của các AI bot: {', '.join(blocked_bots)}.")
        report.append("     Điều này khiến website không thể xuất hiện hoặc được trích dẫn trong AI Overviews và Copilot.")
    else:
        report.append("[✅] **Cấu hình AI tốt**: robots.txt cho phép các AI crawler thu thập dữ liệu bình thường.")
        
    # Kiểm tra Sitemap
    has_sitemap = any(l.startswith('sitemap:') for l in lines)
    if has_sitemap:
        report.append("[✅] **Sitemap**: Đã khai báo đường dẫn Sitemap trong robots.txt.")
    else:
        report.append("[❌] **Thiếu Sitemap**: Chưa cấu hình dòng khai báo Sitemap trong robots.txt.")
        
    return "\n".join(report)

# --- SINH SCHEMA JSON-LD MẪU ---
def generate_schema(schema_type):
    if schema_type == "LocalBusiness":
        schema = {
            "@context": "https://schema.org",
            "@type": "SportsActivityLocation",
            "@id": "https://newton.dayboi.vip/#sportsactivitylocation",
            "name": "Trung tâm dạy bơi CanSwim Bể bơi Newton",
            "image": "https://newton.dayboi.vip/logo.png",
            "telephone": PROJECT_HOTLINE,
            "email": "dayboivip@gmail.com",
            "url": "https://newton.dayboi.vip",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "cuối ngõ 234 Hoàng Quốc Việt, khu Trường Newton, lô TH2 khu đô thị Nam Cường, phường Nghĩa Đô",
                "addressLocality": "quận Cầu Giấy",
                "addressRegion": "Hà Nội",
                "addressCountry": "VN"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": "21.0478",
                "longitude": "105.7924"
            },
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "opens": "06:00",
                "closes": "21:00"
            }
        }
    elif schema_type == "BlogPosting":
        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": "https://newton.dayboi.vip/cam-nang/tieu-de-bai-viet"
            },
            "headline": "Tiêu đề bài viết cẩm nang mẫu",
            "description": "Mô tả ngắn gọn meta description của bài viết cẩm nang...",
            "image": "https://newton.dayboi.vip/images/tuyen-sinh/lop-day-boi-tre-em-cau-giay.png",
            "author": {
                "@type": "Person",
                "name": "Bùi Văn Cán",
                "jobTitle": "HLV Trưởng CanSwim",
                "sameAs": "https://www.linkedin.com/in/thay-bui-van-can-canswim"
            },
            "publisher": {
                "@type": "Organization",
                "name": "CanSwim Bể bơi Newton",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://newton.dayboi.vip/logo.png"
                }
            },
            "datePublished": "2026-05-30",
            "dateModified": "2026-05-30"
        }
    elif schema_type == "FAQPage":
        schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Học bơi tại bể bơi Newton có cam kết biết bơi không?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Có, CanSwim cam kết 100% học viên tốt nghiệp đều biết bơi đúng kỹ thuật. Đối với học viên nhát nước, học chậm sẽ được hỗ trợ kèm thêm miễn phí không phát sinh chi phí cho tới khi biết bơi tốt mới kết thúc."
                    }
                }
            ]
        }
    else:
        return f"Lỗi: Không hỗ trợ kiểu schema '{schema_type}'."
        
    return json.dumps(schema, indent=2, ensure_ascii=False)

# --- HÀM MAIN ---
def main():
    parser = argparse.ArgumentParser(description="CanSwim SEO Checklist Checker & Scorer 2026")
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực hiện")
    
    # check-file
    p_file = subparsers.add_parser("check-file", help="Kiểm tra một file .md hoặc .astro")
    p_file.add_argument("path", help="Đường dẫn tới file cần kiểm tra")
    p_file.add_argument("--keyword", help="Từ khóa chính kiểm tra SEO", default=None)
    p_file.add_argument("--output", help="Đường dẫn lưu file báo cáo", default=None)
    
    # check-dir
    p_dir = subparsers.add_parser("check-dir", help="Kiểm tra hàng loạt file trong thư mục")
    p_dir.add_argument("path", help="Đường dẫn tới thư mục")
    p_dir.add_argument("--output", help="Thư mục xuất báo cáo", default=None)
    
    # check-robots
    p_rob = subparsers.add_parser("check-robots", help="Kiểm tra cấu hình robots.txt")
    p_rob.add_argument("path", help="Đường dẫn tới file robots.txt")
    
    # generate-schema
    p_sch = subparsers.add_parser("generate-schema", help="Sinh Schema JSON-LD mẫu")
    p_sch.add_argument("type", choices=["LocalBusiness", "BlogPosting", "FAQPage"], help="Loại schema")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    if args.command == "check-file":
        res = check_file(args.path, args.keyword)
        if res:
            print(res["report"])
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as out_f:
                    out_f.write(res["report"])
                print(f"\n[✅] Đã xuất báo cáo chi tiết ra: {args.output}")
                
    elif args.command == "check-dir":
        dir_path = Path(args.path)
        if not dir_path.is_dir():
            print(f"Lỗi: {args.path} không phải là thư mục hợp lệ.", file=sys.stderr)
            sys.exit(1)
            
        reports = []
        for file in dir_path.glob('**/*'):
            if file.suffix.lower() in ['.md', '.astro']:
                print(f"Đang kiểm tra: {file.relative_to(dir_path)}")
                res = check_file(str(file))
                if res:
                    reports.append(res)
                    
        print(f"\n=== TỔNG HỢP KẾT QUẢ QUÉT THƯ MỤC ({len(reports)} files) ===")
        summary_md = []
        summary_md.append(f"# BẢO CÁO SEO TỔNG HỢP THƯ MỤC: {dir_path.name}")
        summary_md.append(f"Tổng số file quét: {len(reports)}\n")
        summary_md.append("| Tên File | Số từ | Điểm SEO | Đánh giá |")
        summary_md.append("|---|---|---|---|")
        
        for r in reports:
            status = "🔴 Yếu"
            if r["score"] >= 90:
                status = "🟢 Tốt"
            elif r["score"] >= 70:
                status = "🟡 Trung bình"
            summary_md.append(f"| {Path(r['file']).name} | {r['word_count']} | **{r['score']}/100** | {status} |")
            
        summary_text = "\n".join(summary_md)
        print(summary_text)
        
        if args.output:
            out_file = Path(args.output)
            if out_file.is_dir():
                out_file = out_file / "seo_directory_report.md"
            with open(out_file, 'w', encoding='utf-8') as out_f:
                out_f.write(summary_text)
            print(f"\n[✅] Đã lưu báo cáo tổng hợp ra: {out_file}")
            
    elif args.command == "check-robots":
        res = check_robots(args.path)
        print(res)
        
    elif args.command == "generate-schema":
        res = generate_schema(args.type)
        print(res)

if __name__ == "__main__":
    main()
