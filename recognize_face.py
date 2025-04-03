import cv2
import face_recognition
import pickle
import os
import numpy as np


def load_known_face_encodings(encoding_file="Images/known_face_encodings.pkl"):
    if not os.path.exists(encoding_file):
        print("Encoding file not found. Please save the face encoding first.")
        return None, None

    try:
        with open(encoding_file, "rb") as f:
            known_face_encodings, known_face_names = pickle.load(f)
        print(f"Loaded {len(known_face_encodings)} known face encodings.")
        return known_face_encodings, known_face_names
    except Exception as e:
        print(f"Error loading face encodings: {e}")
        return None, None


def recognize_face_from_camera(encoding_file="Images/known_face_encodings.pkl"):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Unable to open camera.")
        return

    known_face_encodings, known_face_names = load_known_face_encodings(encoding_file)

    if known_face_encodings is None:
        print("No known face encodings available.")
        return

    print("Camera is open. Start recognizing faces...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Unable to capture frame.")
            break

        # Resize ảnh để giảm thời gian xử lý
        frame_small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Phát hiện các khuôn mặt trong ảnh
        face_locations = face_recognition.face_locations(frame_small)
        face_encodings = face_recognition.face_encodings(frame_small, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            color = (0, 0, 255)  # Màu đỏ cho khuôn mặt chưa nhận diện

            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]
                color = (0, 255, 0)  # Màu xanh cho khuôn mặt đã nhận diện

            # Chuyển lại kích thước ban đầu của frame
            top, right, bottom, left = [v * 2 for v in (top, right, bottom, left)]

            # Vẽ khung bao quanh khuôn mặt
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting face recognition.")
            break

    cap.release()
    cv2.destroyAllWindows()
