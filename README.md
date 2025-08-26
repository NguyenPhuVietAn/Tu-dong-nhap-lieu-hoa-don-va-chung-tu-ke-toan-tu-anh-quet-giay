# 🧾 Tự động nhập liệu hóa đơn chứng từ kế toán từ ảnh/PDF

## 📌 Giới thiệu
Đây là ứng dụng hỗ trợ **tự động nhập liệu hóa đơn và chứng từ kế toán** bằng công nghệ **OCR (Optical Character Recognition)** kết hợp với **AI/NLP**.  
Hệ thống cho phép:
- Đọc dữ liệu từ hóa đơn giấy (chụp ảnh, scan) hoặc hóa đơn điện tử (PDF, ảnh).
- Trích xuất các thông tin quan trọng như:
  - Số hóa đơn
  - Ngày phát hành
  - Mã số thuế
  - Tên đơn vị phát hành / nhà cung cấp
  - Giá trị trước thuế, thuế VAT, tổng cộng
- Lưu trữ dữ liệu vào **cơ sở dữ liệu**.
- Cho phép hiệu chỉnh dữ liệu trên giao diện trước khi lưu.
- Xuất dữ liệu ra Excel hoặc đồng bộ với **phần mềm kế toán/ERP** (MISA, FAST, Odoo, SAP...).

Ứng dụng giúp kế toán giảm thời gian nhập liệu thủ công, hạn chế sai sót và tối ưu hóa hiệu quả quản lý tài chính – kế toán trong tiến trình **chuyển đổi số**.

---

## 🏗️ Kiến trúc hệ thống
Hệ thống được thiết kế theo 3 lớp:
1. **Frontend (Web/Desktop UI)**  
   - Upload ảnh/PDF hóa đơn  
   - Hiển thị dữ liệu nhận dạng  
   - Cho phép chỉnh sửa trước khi lưu  

2. **Backend (Flask/Django/.NET API)**  
   - Xử lý OCR (Tesseract / PaddleOCR / Google Vision API)  
   - Trích xuất & chuẩn hóa dữ liệu (Regex + NLP)  
   - Kết nối và ghi dữ liệu vào CSDL  

3. **Database (MySQL/PostgreSQL/SQL Server)**  
   - Lưu trữ hóa đơn, chứng từ, thông tin người dùng  
   - Hỗ trợ đồng bộ dữ liệu với phần mềm kế toán  

---

## ⚙️ Công nghệ & Công cụ sử dụng
| Thành phần       | Công cụ / Thư viện |
|------------------|--------------------|
| Xử lý ảnh        | OpenCV             |
| OCR              | PaddleOCR, Tesseract, Google Vision API |
| Trích xuất dữ liệu | Regex, spaCy (NLP) |
| Lưu trữ          | MySQL, PostgreSQL, SQL Server |
| API backend      | Flask / Django / .NET |
| Giao tiếp        | JSON, REST API |

---

## 🚀 Cài đặt & Chạy thử

### Yêu cầu hệ thống
- Python >= 3.8
- Node.js (nếu chạy frontend web)
- CSDL: MySQL hoặc PostgreSQL hoặc SQL Server
- GPU (khuyến nghị khi dùng PaddleOCR)

### Các bước cài đặt (ví dụ với Python + Flask + MySQL)
```bash
# Clone dự án
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>

# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate   # Linux / MacOS
venv\Scripts\activate      # Windows

# Cài đặt thư viện cần thiết
pip install -r requirements.txt

# Chạy ứng dụng
flask run
