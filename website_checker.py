##############################################################
# PROJECT: WEBSITE STATUS CHECKER
# Mục tiêu: Sử dụng subprocess để kiểm tra trạng thái của các website.
# Kỹ năng: subprocess, list, loop, platform-specific commands.
##############################################################

import subprocess
import platform
import os

def check_website_status():
    """Kiểm tra trạng thái của các website bằng lệnh ping."""
    
    # --- 1. Cấu hình ---
    websites_to_check = [
        "google.com",
        "facebook.com",
        "github.com",
        "a-website-that-does-not-exist.com" # Website không tồn tại để kiểm tra trường hợp lỗi
    ]
    
    print("--- Bắt đầu kiểm tra trạng thái Website ---\n")
    
    # --- 2. Lặp qua danh sách và kiểm tra ---
    for website in websites_to_check:
        # Lệnh ping khác nhau tùy hệ điều hành
        # Windows: ping -n 1 <host>
        # macOS/Linux: ping -c 1 <host>
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', website]
        
        # Chạy lệnh và giấu output bằng cách chuyển nó vào DEVNULL
        # DEVNULL là một cách để "vứt" output đi, tương tự /dev/null trên Linux
        response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # subprocess.call() trả về 0 nếu thành công
        if response == 0:
            print(f"✓ {website:<35} is UP")
        else:
            print(f"✗ {website:<35} is DOWN")

    print("\n--- Kiểm tra hoàn tất ---")

if __name__ == "__main__":
    check_website_status()