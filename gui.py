import tkinter as tk

from save_face import save_new_face
from recognize_face import recognize_face_from_camera



# Giao diện chính
def main():
    window = tk.Tk()
    window.title("Face Recognition System")

    label = tk.Label(window)
    label.pack(pady=20)

    # Nút nhận diện khuôn mặt
    btn_recognize = tk.Button(window, text="Start Recognizing Faces", command=lambda: recognize_face_from_camera())
    btn_recognize.pack(pady=10)

    # Nút lưu khuôn mặt mới
    btn_save = tk.Button(window, text="Save New Face Encoding", command=save_new_face)
    btn_save.pack(pady=10)

    window.mainloop()

