import cv2
import face_recognition
import pickle
import os
import time
import numpy as np
from tkinter import simpledialog, messagebox

def save_face_encoding_from_camera(encoding_file="Images/known_face_encodings.pkl", capture_duration=5, num_images=10):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Unable to open camera.")
        return None, None

    known_face_encodings = []
    known_face_names = []

    # Kiểm tra nếu đã có file lưu face encodings, thì tải lên
    if os.path.exists(encoding_file):
        try:
            with open(encoding_file, "rb") as f:
                known_face_encodings, known_face_names = pickle.load(f)
            print(f"Loaded {len(known_face_encodings)} existing face encodings.")
        except Exception as e:
            print(f"Error loading face encodings: {e}")

    print(f"Camera is open. Capturing face for {capture_duration} seconds...")

    start_time = time.time()
    captured_face = False
    captured_images = []
    captured_face_locations = []

    while len(captured_images) < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Unable to capture frame.")
            break

        cv2.imshow("Captured Face", frame)

        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            captured_images.append(frame)
            captured_face_locations.append(face_locations)

        if len(captured_images) >= num_images or time.time() - start_time > capture_duration:
            captured_face = True
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if captured_face and len(captured_images) >= num_images:
        print(f"Captured {num_images} images with faces.")

        label = simpledialog.askstring("Input", "Enter label for this face (e.g., name or ID):")
        if not label:
            messagebox.showwarning("Warning", "You must provide a name or ID.")
            return None, None

        # Lưu các face encodings từ các ảnh đã chụp
        for i, frame in enumerate(captured_images):
            face_encodings = face_recognition.face_encodings(frame, captured_face_locations[i])
            if face_encodings:
                encoding = face_encodings[0]
                # Kiểm tra lại face encoding
                if isinstance(encoding, np.ndarray) and encoding.shape == (128,):
                    known_face_encodings.append(encoding)

        # Lưu tên vào danh sách known_face_names
        known_face_names.append(label)

        try:
            if not os.path.exists("Images"):
                os.makedirs("Images")
            with open(encoding_file, "wb") as f:
                pickle.dump((known_face_encodings, known_face_names), f)
            print(f"Saved {len(known_face_encodings)} face encodings to file.")
        except Exception as e:
            print(f"Error saving face encodings: {e}")
        return captured_images, captured_face_locations
    else:
        print("Failed to capture enough face images.")
        return None, None


def save_new_face():
    # Sử dụng các giá trị mặc định cho thời gian và số lượng ảnh
    capture_duration = 5  # Thời gian chụp mặc định 5 giây
    num_images = 10  # Số lượng ảnh chụp mặc định là 10

    # Lưu face encoding từ camera với thời gian người dùng đã nhập
    captured_images, captured_face_locations = save_face_encoding_from_camera(capture_duration=capture_duration, num_images=num_images)

    if captured_images is None:
        messagebox.showerror("Error", "No face detected or camera issue!")
        return

    # Chỉ yêu cầu người dùng nhập nhãn trong save_face_encoding_from_camera rồi, không cần yêu cầu lại ở đây
    messagebox.showinfo("Success", "Face encoding saved successfully!")

