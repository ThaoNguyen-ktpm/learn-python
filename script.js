const darkModeBtn = document.getElementById("darkModeBtn");

darkModeBtn.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
});

// Logic cho menu trên di động
const menuBtn = document.querySelector(".menu-btn");
const navLinks = document.querySelector(".navbar ul");

menuBtn.addEventListener("click", () => {
    navLinks.classList.toggle("show");
});

// --- Logic cho các nút Demo ---
document.querySelectorAll('.btn-demo').forEach(button => {
    button.addEventListener('click', (event) => {
        const projectName = event.target.getAttribute('data-project');
        if (projectName === 'website-checker') {
            runWebsiteCheckerDemo();
        }
        if (projectName === 'api-saver') {
            runApiDataSaverDemo();
        }
        if (projectName === 'video-processor') {
            runVideoProcessor();
        }
    });
});

function runWebsiteCheckerDemo() {
    const outputElement = document.getElementById('website-checker-output');
    outputElement.style.display = 'block'; // Hiện khung output
    outputElement.innerHTML = ''; // Xóa nội dung cũ

    const websites = [
        { name: "google.com", status: "UP" },
        { name: "facebook.com", status: "UP" },
        { name: "github.com", status: "UP" },
        { name: "a-website-that-does-not-exist.com", status: "DOWN" }
    ];

    const lines = [
        "--- Bắt đầu kiểm tra trạng thái Website ---",
        ...websites.map(site => `Pinging ${site.name}...`),
        "--- Kết quả ---",
        ...websites.map(site => site.status === "UP" 
            ? `✓ ${site.name.padEnd(35, ' ')} is UP` 
            : `✗ ${site.name.padEnd(35, ' ')} is DOWN`),
        "\n--- Kiểm tra hoàn tất ---"
    ];

    let lineIndex = 0;
    const interval = setInterval(() => {
        if (lineIndex < lines.length) {
            outputElement.innerHTML += lines[lineIndex] + '\n';
            lineIndex++;
        } else {
            clearInterval(interval);
        }
    }, 300); // In mỗi dòng cách nhau 300ms
}

function runApiDataSaverDemo() {
    const outputElement = document.getElementById('api-saver-output');
    outputElement.style.display = 'block';
    outputElement.innerHTML = '';

    const lines = [
        "Đã tạo thư mục: 'api_data'",
        "Đang lấy dữ liệu từ https://jsonplaceholder.typicode.com/users...",
        "✓ Lấy dữ liệu thành công!",
        "✓ Đã lưu dữ liệu đầy đủ vào file: api_data/users.json",
        "✓ Đã lưu dữ liệu tóm tắt vào file: api_data/users.csv",
        "\nHoàn thành! Hãy kiểm tra thư mục 'api_data'."
    ];

    let lineIndex = 0;
    const interval = setInterval(() => {
        if (lineIndex < lines.length) {
            outputElement.innerHTML += lines[lineIndex] + '\n';
            lineIndex++;
        } else {
            clearInterval(interval);
        }
    }, 500); // In mỗi dòng cách nhau 500ms
}

function runVideoProcessor() {
    const outputElement = document.getElementById('video-processor-output');
    const uploadBtn = document.getElementById('video-upload-btn');
    const fileInput = document.getElementById('video-upload-input');

    // Hiển thị giao diện và xóa nội dung cũ
    document.getElementById('video-processor-ui').style.display = 'block';
    outputElement.innerHTML = 'Click "Select Video From Computer" to start...';
    outputElement.style.display = 'block';

    // Khi nhấn nút "Chọn Video", ta kích hoạt input ẩn
    uploadBtn.onclick = () => {
        fileInput.click();
    };

    // Khi người dùng đã chọn xong file, sự kiện 'change' sẽ được kích hoạt
    fileInput.onchange = async (event) => {
        const file = event.target.files[0];
        if (!file) {
            return;
        }

        // Hiển thị trạng thái đang xử lý
        outputElement.innerHTML = `Uploading and processing: ${file.name}...`;
        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Processing...';

        try {
            const formData = new FormData();
            formData.append('video', file);

            const response = await fetch('/api/process-video', {
                method: 'POST',
                body: formData, // Gửi file dưới dạng FormData
            });

            const data = await response.json();
            outputElement.innerHTML = ''; // Xóa thông báo "đang xử lý"

            if (data.success) {
                const result = data.results[0]; // Chỉ có một kết quả vì ta upload 1 file
                result.logs.forEach(log => outputElement.innerHTML += log + '\n');
                if (result.thumbnail) {
                    outputElement.innerHTML += `<img src="${result.thumbnail}" alt="Thumbnail" style="max-width: 200px; margin-top: 10px; border-radius: 5px;">\n`;
                }
            } else {
                outputElement.innerHTML = `Server Error: ${data.error}`;
            }
        } catch (error) {
            outputElement.innerHTML = `Connection Error: ${error}. Make sure you are running 'python app.py'.`;
        } finally {
            // Kích hoạt lại nút và reset input
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Select Video From Computer';
            fileInput.value = ''; // Reset để có thể chọn lại cùng một file
        }
    };
}