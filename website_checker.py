##############################################################
# PROJECT: WEBSITE STATUS CHECKER
# Mục tiêu: Sử dụng subprocess để kiểm tra trạng thái của các website.
# Kỹ năng: subprocess, list, loop, platform-specific commands.
##############################################################

import subprocess
import platform
import concurrent.futures

def check_single_website(website):
    """
    Kiểm tra trạng thái của một website duy nhất bằng lệnh ping.
    Trả về một tuple chứa (website, status).
    """
    try:
        # Lệnh ping khác nhau tùy hệ điều hành
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', website]
        
        # subprocess.run là cách tiếp cận hiện đại hơn so với subprocess.call
        # check=True sẽ ném ra ngoại lệ CalledProcessError nếu lệnh trả về mã lỗi (khác 0)
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return (website, "UP")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # CalledProcessError: ping thất bại (host không tồn tại)
        # FileNotFoundError: lệnh ping không tồn tại trên hệ thống
        return (website, "DOWN")

def check_website_status():
    """Kiểm tra trạng thái của các website bằng lệnh ping."""
    
    websites_to_check = [
        "google.com",
        "facebook.com",
        "github.com",
        "youtube.com",
        "vnexpress.net",
        "a-website-that-does-not-exist.com" # Website không tồn tại để kiểm tra trường hợp lỗi
    ]
    
    print("--- Bắt đầu kiểm tra trạng thái Website ---\n")
    
    # Sử dụng ThreadPoolExecutor để chạy các kiểm tra đồng thời
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(websites_to_check)) as executor:
        # Gửi các tác vụ kiểm tra website vào pool
        future_to_website = {executor.submit(check_single_website, website): website for website in websites_to_check}
        for future in concurrent.futures.as_completed(future_to_website):
            website, status = future.result()
            if status == "UP":
                print(f"✓ {website:<35} is UP")
            else:
                print(f"✗ {website:<35} is DOWN")

    print("\n--- Kiểm tra hoàn tất ---")

if __name__ == "__main__":
    check_website_status()