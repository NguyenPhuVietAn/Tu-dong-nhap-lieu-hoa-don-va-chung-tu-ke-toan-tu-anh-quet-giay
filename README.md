# Invoice Extractor App

Ứng dụng demo nhận diện và trích xuất dữ liệu hóa đơn/chứng từ từ ảnh bằng AI + OCR.

## Cách sử dụng

1. Cài đặt các thư viện:
   ```
   pip install -r requirements.txt
   ```
2. Cài đặt Tesseract OCR:
   - Tải từ https://github.com/tesseract-ocr/tesseract
   - Thêm đường dẫn vào biến môi trường (PATH).
3. Chạy ứng dụng Flask:
   ```
   set FLASK_APP=app
   flask run
   ```
4. Truy cập trang web, upload ảnh hóa đơn, xem kết quả nhận diện.

## Cấu trúc thư mục

- app/
  - __init__.py
  - routes.py
  - utils/
    - image_processing.py
  - templates/
    - index.html
- requirements.txt
- README.md
