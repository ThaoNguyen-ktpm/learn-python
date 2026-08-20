import os
import sys
import uuid
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Thêm thư mục hiện tại vào Python path để có thể import các script khác
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import hàm xử lý chính từ video_processor
# Chúng ta sẽ cần sửa đổi video_processor.py một chút để nó trả về kết quả thay vì in ra
from video_processor import process_video_for_api

app = Flask(__name__, static_folder=None) # Tắt static folder mặc định

# --- API Endpoint để xử lý video ---
@app.route('/api/process-video', methods=['POST'])
def handle_video_upload():
    # 1. Kiểm tra xem có file được gửi lên không
    if 'video' not in request.files:
        return jsonify({"success": False, "error": "No file was uploaded."}), 400

    file = request.files['video']

    if file.filename == '':
        return jsonify({"success": False, "error": "No file was selected."}), 400

    # 2. Tạo thư mục upload tạm thời nếu chưa có
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # 3. Lưu file vào thư mục tạm
    # Sử dụng tên file an toàn và thêm UUID để tránh trùng lặp
    original_filename = secure_filename(file.filename)
    temp_filename = f"{uuid.uuid4()}_{original_filename}"
    temp_filepath = os.path.join(upload_folder, temp_filename)
    
    try:
        file.save(temp_filepath)

        # 4. Gọi hàm xử lý video với đường dẫn của file tạm
        results = process_video_for_api(temp_filepath)

        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": f"An error occurred during processing: {str(e)}"}), 500
    finally:
        # 5. Xóa file tạm sau khi đã xử lý xong
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

# --- Route để phục vụ các file tĩnh (HTML, CSS, JS) ---
@app.route('/')
def serve_index():
    # Giả sử file HTML của bạn tên là index.html và nằm cùng cấp
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    # Phục vụ các file như script.js, style.css
    return send_from_directory('.', filename)

# --- Route để phục vụ các ảnh thumbnail đã tạo ra ---
@app.route('/video_output/<path:filename>')
def serve_video_output(filename):
    return send_from_directory('video_output', filename)


def run_app():
    print("--- Server đang chạy! ---")
    print("Mở trình duyệt và truy cập: http://127.0.0.1:5000")
    print("Nhấn CTRL+C để dừng server.")
    # host='0.0.0.0' cho phép truy cập từ các thiết bị khác trong cùng mạng
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    # Lưu ý: Khi chạy ở chế độ debug, Flask sẽ tự khởi động lại khi có thay đổi.
    # Nó có thể chạy hàm run_app() hai lần, điều này là bình thường.
    run_app()