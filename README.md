# Tổng quan về dự án: 
## Mục đích:
- Giảm thời gian các giao dịch xảy ra tại căn tin trường học.
- Tự động hóa bước thanh toán thay vì thủ công như trước.

## Chức năng:
- Nhận diện thức ăn trong khay thông qua camera.
- Tính giá tiền tự động.
- Tính giá trị dinh dưỡng tổng bữa ăn
- Hỗ trợ phương thức thanh toán.

# Hướng dẫn cài đặt:
- Tải các file cần thiết bao gồm code "canteen_food_detect.py và model "best_value_canteen_food_4.pt"
- Tải thư mục UI để giao diện có thể hoạt động.

# Hướng dẫn sử dụng:
### 1. Chạy code trên các nền tảng hỗ trợ file python.

### 2. Sau khi chạy chương trình sẽ hiện ra màn hình bắt đầu.
- Nhấn Start -> Chuyển sang màn hình nhận diện.
- Nhất Exit -> Thoát chương trình.

### 3. Màn hình nhận diện sẽ hiện ra, lúc đó đưa khay thức ăn vào để bắt đầu nhận diện. Giá tiền và giá trị dinh dưỡng sẽ hiển thị bên phải.
- Capture -> Chụp khay thức ăn lại để nhận diện.
- Cancel -> Chụp lại nếu ảnh chưa chính xác.
- Return -> Quay lại màn hình bắt đầu.
- Pay -> Chuyển sang màn hình thanh toán.

### 4. Màn hình thanh toán bao gồm 2 phương thức thanh toán, chọn 1 trong 2 và thanh toán sẽ chuyển sang giao diện cảm ơn.
- QR
- Cash

### 5. Màn hình cảm ơn:
- Home -> Quay lại màn hình bắt đầu.
- Return -> Quay lại màn hình nhận diện.
- Exit -> Thoát chương trình.

# Các phần phụ thuộc:
- Yêu cầu tải các mục tại hướng dẫn cài đặt.
- Cài thư viện ultralystics.
