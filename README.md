# Invoice Extractor App

Ứng dụng demo nhận diện và trích xuất dữ liệu hóa đơn/chứng từ từ ảnh bằng AI + OCR.
## 1. Giới thiệu
`Invoice Extractor App` là ứng dụng demo viết bằng Flask cho phép người dùng tải ảnh hóa đơn/chứng từ lên, thực hiện OCR và áp dụng logic trích xuất để lấy các trường quan trọng (ví dụ: mã hóa đơn, ngày, tổng tiền, thuế, tên nhà cung cấp...). Ứng dụng kết hợp Tesseract OCR cho việc nhận dạng ký tự và các bước xử lý ảnh + quy tắc (hoặc mô hình ML) để trích xuất thông tin có cấu trúc.

Mục tiêu:

* Minh họa pipeline OCR cơ bản cho hoá đơn.
* Dễ cài đặt, dễ mở rộng.
* Cung cấp nơi để thử nghiệm các thuật toán tiền xử lý và trích xuất.

## 2. Yêu cầu hệ thống

* Python 3.8+ (khuyến nghị 3.10+)
* pip
* Tesseract OCR (chạy trên hệ điều hành của bạn)
* Thư viện Python (xem `requirements.txt`)

Phần cứng:

* Máy phát triển bình thường có thể chạy được. Để xử lý hàng loạt hoặc mô hình ML nặng, máy có GPU/CPU mạnh hơn sẽ tốt hơn.

## 3. Cài đặt nhanh

1. Clone repo:

   ```bash
   git clone <repo-url>
   cd invoice-extractor-app
   ```
2. Tạo môi trường ảo (khuyến nghị):

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows
   ```
3. Cài đặt các thư viện Python:

   ```bash
   pip install -r requirements.txt
   ```
4. Cài đặt Tesseract OCR (chi tiết ở phần 4)

## 4. Cấu hình Tesseract

* Tải Tesseract từ trang chính thức: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
* Cài đặt theo hướng dẫn dành cho hệ điều hành của bạn.
* Windows: sau khi cài, thêm đường dẫn `C:\Program Files\Tesseract-OCR` (hoặc nơi bạn cài) vào biến môi trường `PATH`.
* macOS: có thể cài qua Homebrew: `brew install tesseract`.
* Linux (Ubuntu): `sudo apt-get install tesseract-ocr`.

Trong mã Python, bạn có thể chỉ định đường dẫn thủ công nếu không có trong `PATH`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Ngoài ra, nếu cần nhận dạng ngôn ngữ khác (ví dụ tiếng Việt), hãy cài gói ngôn ngữ phù hợp (ví dụ `tessdata` cho tiếng việt):

```
# Ubuntu example
sudo apt-get install tesseract-ocr-vie
```

Và gọi khi OCR:

```python
text = pytesseract.image_to_string(img, lang='vie')
```

## 5. Cấu trúc thư mục

```
- app/
  - __init__.py        # Khởi tạo Flask app
  - routes.py          # Định nghĩa route (upload, xem kết quả...)
  - utils/
    - image_processing.py  # Hàm tiền xử lý ảnh, resize, threshold, deskew...
    - ocr.py               # Wrapper gọi pytesseract, map kết quả
    - extractor.py         # Logic trích xuất các trường (regex, key-value, layout)
  - templates/
    - index.html        # Giao diện upload và hiển thị kết quả
    - result.html       # Hiển thị kết quả chi tiết
- requirements.txt
- README.md
- static/              # (nếu có) css, js, các file tĩnh
```

## 6. Mô tả chi tiết các thành phần

### `app/__init__.py`

* Tạo và cấu hình Flask app, khởi tạo các biến môi trường, logging, cấu hình upload folder.

### `app/routes.py`

* Route chính:

  * `GET /` : trang upload
  * `POST /upload` : nhận file ảnh, lưu tạm, gọi pipeline xử lý, trả về kết quả
  * `GET /result/<id>` : xem kết quả đã xử lý
* Xử lý file upload: kiểm tra định dạng (jpg, png, jpeg, pdf), kích thước tối đa.

### `app/utils/image_processing.py`

Chứa các hàm tiền xử lý ảnh để nâng cao chất lượng OCR:

* `load_image(path)` : đọc ảnh (OpenCV / PIL)
* `to_grayscale(img)`
* `deskew(img)` : hiệu chỉnh nghiêng
* `binarize(img, method='adaptive')`
* `denoise(img)` : lọc nhiễu
* `resize_with_aspect(img, max_dim=2000)` : nhân kích thước để OCR tốt hơn
* `sharpen(img)`

Gợi ý: tổ chức pipeline tiền xử lý thành các bước có thể bật/tắt bằng tham số để thử nghiệm.

### `app/utils/ocr.py`

* Wrapper gọi `pytesseract.image_to_string` hoặc `image_to_data` để thu thập text và bounding boxes.
* Tùy chọn: `lang`, `config` (ví dụ `--psm`), trả về cả `raw_text` và `structured_data`.

Ví dụ `image_to_data` trả về dataframe với cột `left, top, width, height, text, conf` — hữu ích khi làm map key-value theo tọa độ.

### `app/utils/extractor.py`

* Logic trích xuất các trường:

  * Dùng kết hợp regex (ví dụ pattern cho mã hóa đơn, tổng tiền, ngày), từ khoá ("Tổng cộng", "Total"), và mapping vị trí (gần top-right, bottom...) project-specific.
  * Cách tiếp cận phổ biến:

    1. Lấy toàn bộ văn bản OCR.
    2. Chuẩn hoá (loại bỏ ký tự đặc biệt, chuyển chữ thường/hoa phù hợp).
    3. Tìm theo từ khoá để lấy giá trị liền kề hoặc trong cùng dòng.
    4. Nếu có bounding boxes, tìm cặp key-value dựa trên khoảng cách giữa boxes.
    5. Áp dụng các rule kiểm tra (validate date format, parse tiền bằng regex, loại bỏ giá trị không hợp lệ).

* Trả về JSON với các trường: `invoice_number, date, vendor, total, tax, currency, line_items[]`.

## 7. Chạy ứng dụng

1. Đặt biến môi trường (Windows):

```bash
set FLASK_APP=app
set FLASK_ENV=development   # tuỳ chọn
flask run
```

macOS / Linux:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

2. Mặc định ứng dụng chạy ở `http://127.0.0.1:5000`.
3. Truy cập trang, upload ảnh và xem kết quả.

## 8. Giao diện web và API

### Giao diện web (templates)

* `index.html` : form upload, hiển thị lịch sử upload gần nhất, các tuỳ chọn tiền xử lý (checkbox bật/tắt deskew, denoise...).
* `result.html` : hiển thị ảnh gốc, overlay bounding boxes (nếu dùng), raw OCR text, và bảng kết quả trích xuất.

### API (tùy triển khai)

* `POST /api/extract`

  * Payload: multipart-form file
  * Response: JSON { success: true, id: "...", data: { invoice\_number: ..., total: ... }, debug: { raw\_text: "..." }}

* `GET /api/result/<id>` => JSON kết quả đã lưu

Đảm bảo API trả về thông tin debug tuỳ chọn (`raw_text`, `confidences`) chỉ khi môi trường là development.

## 9. Xử lý ảnh & tiền xử lý (chi tiết)

Một pipeline tiền xử lý mẫu nên gồm:

1. Chuyển về grayscale.
2. Resize (nếu quá nhỏ) để đảm bảo chữ có đủ điểm ảnh cho OCR — thường giữ chiều dài lớn nhất \~1500-2000 px.
3. Dùng `bilateralFilter` hoặc `fastNlMeansDenoising` để giảm nhiễu.
4. Adaptive thresholding (nếu background không đều).
5. Deskew: tính góc nghiêng bằng moments/Hough transform.
6. Morphological operations (open/close) để nối hoặc tách ký tự.

Thử nghiệm mỗi bước vì một số hoá đơn có gradient nền hoặc watermark — một vài bước có thể làm hỏng OCR.

## 10. Trích xuất dữ liệu & logic hậu xử lý

* Ngôn ngữ: sử dụng regex chuẩn hoá cho tiền tệ (`[\d.,]+`), ngày (`\d{1,2}[\-/]\d{1,2}[\-/]\d{2,4}`) với parse bằng `dateutil.parser`.
* Xử lý chữ số nhầm lẫn: thường OCR nhầm `O` <-> `0`, `I` <-> `1`, `S` <-> `5`. Áp dụng một bước clean-up có điều kiện (ví dụ trong phần giá chỉ giữ chữ số, dấu `.,`).
* Line items: nếu muốn trích xuất từng dòng (mặt hàng, số lượng, đơn giá, thành tiền), cần mapping dựa theo layout (các cột x-position tương đồng). Sử dụng clustering theo `y` coordinate để nhóm các dòng.

## 11. Ví dụ đầu ra mẫu

```json
{
  "invoice_number": "HD-2025-00123",
  "date": "2025-08-20",
  "vendor": "Công ty ABC",
  "total": 1250000.0,
  "tax": 125000.0,
  "currency": "VND",
  "line_items": [
    {"description": "Sản phẩm A", "qty": 2, "unit_price": 500000, "amount": 1000000},
    {"description": "Phí vận chuyển", "qty": 1, "unit_price": 250000, "amount": 250000}
  ]
}
```

## 12. Tinh chỉnh, hiệu năng và tip nâng cao

* Thay Tesseract bằng dịch vụ OCR thương mại (Google Vision, AWS Textract, Azure OCR) nếu cần độ chính xác cao hơn.
* Dùng mô hình deep learning (layoutLM, Donut, TrOCR) cho các hóa đơn phức tạp, chú ý: cần dữ liệu gán nhãn để fine-tune.
* Thực hiện batch processing và queue (Celery + Redis) khi xử lý số lượng nhiều.
* Caching kết quả đã xử lý, lưu raw OCR và kết quả trích xuất để dễ debug.
* Thêm một giao diện chỉnh sửa kết quả (human-in-the-loop) để người dùng sửa kết quả sai và dùng dữ liệu sửa đó để fine-tune quy tắc hoặc huấn luyện mô hình.

## 13. Kiểm tra lỗi & khắc phục sự cố (Troubleshooting)

* **Kết quả OCR rỗng / rất xấu**: kiểm tra ảnh đầu vào (kích thước, blur), thử bật/ tắt các bước tiền xử lý, tăng kích thước ảnh trước khi OCR.
* **Tesseract không tìm thấy**: kiểm tra biến môi trường PATH, hoặc set `pytesseract.pytesseract.tesseract_cmd` trực tiếp.
* **Ngày/tiền không parse được**: kiểm tra regex và bước clean-up (các ký tự lạ), in `raw_text` để debug.
* **Conf low**: khi dùng `image_to_data`, kiểm tra cột `conf`. Lọc những token có `conf` thấp và kiểm tra lại bằng rule hoặc giao diện con người.

## 14. Bảo mật

* Giới hạn kích thước file upload.
* Kiểm tra loại file và không thực thi file upload.
* Lưu dữ liệu nhạy cảm (hóa đơn có thông tin cá nhân) trong storage an toàn; nếu cần, mã hoá khi lưu.
* Ghi log thận trọng; tránh in ra thông tin nhạy cảm trong logs production.

## 15. Đóng gói & triển khai (production)

* Sử dụng WSGI server (gunicorn/uvicorn) thay vì `flask run`.
* Dùng reverse proxy (nginx) để phục vụ static và proxy tới ứng dụng Flask.
* Lưu file tạm trên storage ổn định (S3 hoặc file share) nếu xử lý lớn.
* Triển khai job queue (Celery + Redis/RabbitMQ) cho xử lý bất đồng bộ và reset status tiến trình.
* Thêm health-check endpoint `/healthz`.

### Mẫu `requirements.txt` gợi ý

```
Flask>=2.0
pytesseract
opencv-python
Pillow
numpy
pandas
python-dateutil
...

### Kết luận

README này cung cấp hướng dẫn chi tiết để thiết lập và phát triển tiếp `Invoice Extractor App`. Bạn có thể thêm phần hướng dẫn đóng góp, test case, hoặc ví dụ dataset để giúp người khác dễ dàng tái tạo kết quả. Nếu bạn muốn mình tạo file `CONTRIBUTING.md`, `Dockerfile`, hoặc `docker-compose.yml` để triển khai nhanh, mình sẽ bổ sung tiếp.


