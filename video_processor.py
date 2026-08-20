##############################################################
# PROJECT: VIDEO INFO & THUMBNAIL EXTRACTOR
# Mục tiêu: Lấy thông tin video bằng FFprobe và trích xuất thumbnail bằng OpenCV.
# Kỹ năng: subprocess, json, opencv-python.
##############################################################

import platform
import subprocess
import json
import cv2
import os
import sys

def process_video(video_path, output_logs=True):
    """
    Trích xuất thông tin và tạo ảnh thumbnail cho một file video.
    Trả về một dictionary chứa log và đường dẫn thumbnail.
    """
    if not os.path.exists(video_path):
        log_msg = f"ERROR: Video file not found at '{video_path}'"
        if output_logs: print(log_msg)
        return {"logs": [log_msg], "thumbnail": None}

    output_dir = "video_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # --- 1. Dùng ffprobe (một phần của FFmpeg) để lấy thông tin video ---
    if output_logs: print(f"--- Getting info from: {video_path} ---")
    logs = [f"--- Getting info from: {os.path.basename(video_path)} ---"]
    try:
        # Xác định lệnh ffprobe, ưu tiên đường dẫn tuyệt đối trên Windows
        ffprobe_cmd = 'ffprobe'
        if platform.system() == 'Windows' and os.path.exists('C:/ffmpeg/bin/ffprobe.exe'):
            ffprobe_cmd = 'C:/ffmpeg/bin/ffprobe.exe'

        command = [
            ffprobe_cmd, 
            '-v', 'quiet', 
            '-print_format', 'json',
            '-show_format', '-show_streams', video_path
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        video_info = json.loads(result.stdout)
        
        # Tìm video stream để lấy thông tin chính xác
        video_stream = None
        for stream in video_info.get('streams', []):
            if stream.get('codec_type') == 'video':
                video_stream = stream
                break
        
        if not video_stream:
            log_msg = "ERROR: No video stream found in the file."
            if output_logs: print(log_msg)
            return {"logs": logs + [log_msg], "thumbnail": None}

        # In ra một vài thông tin hữu ích
        duration = float(video_info['format']['duration'])
        width = video_stream['width']
        height = video_stream['height']
        rotation = video_stream.get('tags', {}).get('rotate', '0')
        
        logs.append(f"✓ Duration: {duration:.2f} seconds")
        logs.append(f"✓ Resolution: {width}x{height}")
        if rotation != '0':
            logs.append(f"✓ Rotation: {rotation} degrees")

    except (subprocess.CalledProcessError, FileNotFoundError):
        log_msg = "ERROR: Could not run ffprobe. Make sure FFmpeg is installed and in your PATH."
        if output_logs: print(log_msg)
        return {"logs": logs + [log_msg], "thumbnail": None}

    # --- 2. Dùng OpenCV để trích xuất frame đầu tiên làm thumbnail ---
    logs.append("\n--- Generating thumbnail ---")
    vid_capture = cv2.VideoCapture(video_path)
    success, image = vid_capture.read()
    thumbnail_url = None

    if success:
        # Xử lý xoay ảnh nếu video có metadata rotation
        if rotation == '90':
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif rotation == '270':
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif rotation == '180':
            image = cv2.rotate(image, cv2.ROTATE_180)

        thumbnail_path = os.path.join(output_dir, f"{os.path.basename(video_path)}_thumbnail.jpg")
        cv2.imwrite(thumbnail_path, image)
        logs.append(f"✓ Thumbnail saved at: {thumbnail_path}")
        # Tạo URL tương đối để trình duyệt có thể hiển thị
        thumbnail_url = thumbnail_path.replace('\\', '/')
    else:
        logs.append("ERROR: Could not read video with OpenCV.")
    
    # In ra console nếu cần
    if output_logs:
        for log in logs:
            print(log)

    return {"logs": logs, "thumbnail": thumbnail_url}

def process_video_for_api(input_path):
    """
    Hàm bao bọc để xử lý một file hoặc một thư mục cho API.
    """
    VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']
    all_results = []

    if os.path.isdir(input_path):
        all_results.append({"logs": [f"--- Starting batch processing in directory: {input_path} ---"], "thumbnail": None})
        for filename in os.listdir(input_path):
            if any(filename.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
                video_file_path = os.path.join(input_path, filename)
                result = process_video(video_file_path, output_logs=False)
                all_results.append(result)
        all_results.append({"logs": ["--- Batch processing complete! ---"], "thumbnail": None})
    elif os.path.isfile(input_path):
        result = process_video(input_path, output_logs=False)
        all_results.append(result)
    else:
        all_results.append({"logs": [f"ERROR: Path does not exist or is invalid: '{input_path}'"], "thumbnail": None})

    return all_results

if __name__ == "__main__":
    # Giữ lại logic cũ để có thể chạy từ dòng lệnh như trước
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        # Chạy hàm mới, nhưng với chế độ in ra console
        results = process_video_for_api(input_path)
        for res in results:
            for log in res['logs']:
                print(log)
            if res.get('thumbnail'):
                print(f"  -> Thumbnail: {res['thumbnail']}")
            print("-" * 40)
    else:
        print("Usage (CLI): python video_processor.py <path_to_video_file_OR_directory>")
        print("Usage (Web): python app.py")
        sys.exit(1)