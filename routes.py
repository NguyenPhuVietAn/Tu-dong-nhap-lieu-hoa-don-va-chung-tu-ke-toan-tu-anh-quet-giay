from flask import render_template, request, jsonify, send_file
from app import app

import cv2
import pandas as pd
from app.utils.image_processing import preprocess_image
from google import genai

# Cấu hình API key cho Gemini
client = genai.Client(api_key="AIzaSyCDp7v0xYjTB9GPu9tLH69qD2kvrTydUAo")

def analyze_invoice_with_gemini(filepath):
    # Hàm này sẽ gửi ảnh lên Gemini AI để phân tích
    my_file = client.files.upload(file=filepath)
    
    prompt = (
        "Hãy phân tích ảnh hóa đơn/chứng từ sau và trả về dạng JSON với tất cả các trường trong ảnh / hóa đơn / chứng từ bằng tiếng Việt.\n"
        "Yêu cầu:\n"
        "1. Chỉ trả về JSON thuần túy, không kèm giải thích\n"
        "2. Các giá trị tiền tệ để dạng số nguyên, không định dạng phân cách\n"
        "3. Đảm bảo encoding UTF-8 cho tiếng Việt\n"
        "4. Tất cả key trong JSON phải không dấu (VD: 'tong_tien', 'dia_chi', 'san_pham')"
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[my_file, prompt]
    )
    
    import re, json
    match = re.search(r'\{.*\}', response.text, re.DOTALL)
    if match:
        try:
            # Decode JSON với encoding UTF-8
            json_text = match.group().encode('utf-8').decode('utf-8')
            return json.loads(json_text, strict=False)
        except Exception as e:
            print(f"Lỗi parse JSON: {str(e)}")
            return {}
    return {}


import os
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
EXCEL_PATH = os.path.join(APP_ROOT, 'output.xlsx')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    image_url = None
    if request.method == 'POST':
        file = request.files['invoice']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        # Gửi ảnh trực tiếp lên Gemini AI để phân tích
        data = analyze_invoice_with_gemini(filepath)
        # Chuyển đổi data sang UTF-8 trước khi lưu Excel
        if data:
            # Chuyển các giá trị về unicode
            data = {k: v.encode('utf-8').decode('utf-8') if isinstance(v, str) else v 
                   for k, v in data.items()}
            # Lưu ra Excel với đường dẫn tuyệt đối
            df = pd.DataFrame([data])
            with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
        image_url = f'/uploads/{filename}'
        return render_template('index.html', data=data, image_url=image_url)
    return render_template('index.html', data=data, image_url=image_url)

# Route phục vụ file ảnh đã upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

# Route tải về file Excel kết quả
@app.route('/download_excel')
def download_excel():
    if os.path.exists(EXCEL_PATH):
        return send_file(EXCEL_PATH, as_attachment=True, download_name='ketqua.xlsx')
    return "File Excel chưa được tạo", 404
