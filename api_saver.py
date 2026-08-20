##############################################################
# PROJECT: API DATA SAVER
# Mục tiêu: Lấy dữ liệu từ một API công khai và lưu dưới dạng JSON và CSV.
# Kỹ năng: requests, json, csv, os.
##############################################################

import requests
import json
import csv
import os

def fetch_and_save_user_data():
    """
    Lấy dữ liệu người dùng từ API và lưu vào các file JSON và CSV.
    """
    api_url = "https://jsonplaceholder.typicode.com/users"
    output_dir = "api_data"

    # --- 1. Tạo thư mục output nếu chưa có ---
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Đã tạo thư mục: '{output_dir}'")
    except OSError as e:
        print(f"LỖI: Không thể tạo thư mục '{output_dir}': {e}")
        return

    # --- 2. Lấy dữ liệu từ API ---
    print(f"Đang lấy dữ liệu từ {api_url}...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Ném ra lỗi nếu request không thành công (status code không phải 2xx)
        users = response.json()
        print("✓ Lấy dữ liệu thành công!")
    except requests.exceptions.RequestException as e:
        print(f"LỖI: Không thể lấy dữ liệu từ API: {e}")
        return

    # --- 3. Lưu dữ liệu đầy đủ vào file JSON ---
    json_path = os.path.join(output_dir, "users.json")
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        print(f"✓ Đã lưu dữ liệu đầy đủ vào file: {json_path}")
    except IOError as e:
        print(f"LỖI: Không thể ghi file JSON: {e}")

    # --- 4. Lưu dữ liệu tóm tắt vào file CSV ---
    csv_path = os.path.join(output_dir, "users.csv")
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'username', 'email', 'website']) # Header
            for user in users:
                writer.writerow([user['id'], user['name'], user['username'], user['email'], user['website']])
        print(f"✓ Đã lưu dữ liệu tóm tắt vào file: {csv_path}")
    except (IOError, csv.Error) as e:
        print(f"LỖI: Không thể ghi file CSV: {e}")

    print(f"\nHoàn thành! Hãy kiểm tra thư mục '{output_dir}'.")

if __name__ == "__main__":
    fetch_and_save_user_data()