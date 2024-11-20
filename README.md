
## Hướng Dẫn Cài Đặt

1. **Download**:
   ```bash
   git clone https://github.com/Hu2Hoang/image-processing-api.git
   cd image-processing-api

2. **Cài thư viện**
    ```bash
    pip install -r requirements.txt
3. **Khởi tạo API**
   ```bash
   python api_pre.py
4.  **Test API**
    ```bash
    curl -X POST http://127.0.0.1:5000/upload \
    -H "Content-Type: multipart/form-data" \
    -F "file=@<đường dẫn file>"
    ```
    Ví dụ
    ```bash
    curl -X POST http://127.0.0.1:5000/upload \
    -H "Content-Type: multipart/form-data" \
    -F "file=@20240928_133751.jpg"
    ```

    Test form upload UI/UX
    ```bash
    index.html - Live Server