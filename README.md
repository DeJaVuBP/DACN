# MÔN ĐỒ ÁN CHUYÊN NGÀNH
# Đề tài: Cài đặt Face ID vào hệ điều hành Windows

## Giới thiệu
Face ID là một công nghệ nhận diện khuôn mặt dựa trên AI, giúp tăng cường bảo mật và tối ưu trải nghiệm người dùng. Đề tài này nhằm tích hợp Face ID vào hệ điều hành Windows, cho phép người dùng đăng nhập bằng khuôn mặt một cách nhanh chóng và an toàn.

## Tính năng chính
- **Nhận diện khuôn mặt:** Sử dụng AI và Machine Learning để xác định danh tính.

## Yêu cầu hệ thống
- **Hệ điều hành:** Windows 10/11
- **Phần cứng:** Camera có khả năng nhận diện 3D
- **Phần mềm:** Python 3.8+, OpenCV, dlib, Face Recognition API

## Cài đặt
1. Cài đặt Python và các thư viện cần thiết:
   ```sh
   pip install opencv-python dlib face-recognition numpy
   ```
2. Kiểm tra camera trên hệ thống:
   ```sh
   python test_camera.py
   ```
3. Chạy chương trình nhận diện khuôn mặt:
   ```sh
   python main.py
   ```

## Ghi chú
- Dự án này đang trong giai đoạn nghiên cứu và phát triển.



