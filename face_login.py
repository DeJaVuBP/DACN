import cv2
import dlib
import numpy as np
import face_recognition
import pyodbc
from tkinter import messagebox


class FaceLogin:
    def __init__(self, root, emp_no):
        self.root = root
        self.emp_no = emp_no
        self.cap = None
        self.stop_event = None

    def login_face(self):
        if not self.emp_no or self.emp_no == "Unknown":
            messagebox.showerror("Error", "Cannot login without an employee ID!", parent=self.root)
            return

        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot open the camera!", parent=self.root)
                return

            detector = dlib.get_frontal_face_detector()
            cv2.namedWindow("Face Login")

            def recognize_face():
                if self.stop_event:
                    return

                ret, frame = self.cap.read()
                if not ret:
                    return

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_frame, model="hog")
                if not face_locations:
                    cv2.putText(frame, "No face detected", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow("Face Login", frame)
                    self.root.after(10, recognize_face)
                    return

                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                face_encoding = face_recognition.face_encodings(rgb_frame, [face_locations[0]])
                if face_encoding:
                    face_encoding = np.array(face_encoding[0], dtype=np.float64).tobytes()
                    if self.verify_face(face_encoding):
                        messagebox.showinfo("Success", f"Login successful for {self.emp_no}!", parent=self.root)
                    else:
                        messagebox.showerror("Error", "Face recognition failed!", parent=self.root)

                cv2.imshow("Face Login", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    self.stop_face_scan()
                    return

                self.root.after(10, recognize_face)

            recognize_face()
            self.root.protocol("WM_DELETE_WINDOW", self.stop_face_scan)

        except Exception as e:
            messagebox.showerror("Error", f"System error: {str(e)}", parent=self.root)

    def verify_face(self, face_encoding):
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'DESKTOP-AHFDNV5\\SQLEXPRESS'
                'DATABASE=Face_ID_Management;'
                'Trusted_Connection=yes;'
            )
            cursor = conn.cursor()

            cursor.execute("SELECT Face_ID FROM Employee WHERE Emp_No = ?", (self.emp_no,))
            row = cursor.fetchone()
            if row:
                stored_face_encoding = np.frombuffer(row[0], dtype=np.float64)
                match = face_recognition.compare_faces([stored_face_encoding], face_encoding)
                return match[0]
            else:
                return False

        except pyodbc.Error as sql_err:
            print(f"[SQL ERROR] {sql_err}")
            return False
        except Exception as ex:
            print(f"[SYSTEM ERROR] {ex}")
            return False
        finally:
            cursor.close()
            conn.close()

    def stop_face_scan(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.stop_event = True
