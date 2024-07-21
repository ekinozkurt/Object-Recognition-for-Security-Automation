import cv2
from datetime import datetime
from detecto.core import Model
import sqlite3
import serial
import time
import subprocess

class Detector(object):
    def __init__(self):
        self._model = Model()

    def predict(self, img):
        return self._model.predict(img)

class LaptopCamera(object):
    def __init__(self, device_id, width=320, height=320):
        self._device_id = device_id
        self._device = cv2.VideoCapture(device_id)
        self._device.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._device.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def __del__(self):
        self._device.release()

    def get_frame(self):
        ret, frame = self._device.read()
        if ret:
            return frame
        else:
            print("No image received!")
            return None

class DetectorNode(object):
    def __init__(self, node_name, camera, detector, threshold, db_file, arduino_serial_port, rfid_serial_port):
        self._camera = camera
        self._detector = detector
        self._threshold = threshold
        self._db_file = db_file
        self._ser = serial.Serial(arduino_serial_port, 9600)
        self._rfid_ser = serial.Serial(rfid_serial_port, 9600)
        print("Serial connection established with Arduinos")

        # Veritabanı bağlantısını oluştur
        self._conn = sqlite3.connect(db_file)
        self._cursor = self._conn.cursor()

        # Tablo oluştur
        self._cursor.execute('''CREATE TABLE IF NOT EXISTS detected_objects
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              product TEXT NOT NULL,
                              category TEXT NOT NULL,
                              detection_time TEXT NOT NULL)''')
        self._conn.commit()
        
        self.user_interface_process = None

    def run(self):
        while True:
            self.check_rfid_commands()
            frame = self._camera.get_frame()
            if frame is None:
                continue
            predictions = self._detector.predict(frame)
            detected_objects = self.draw_bbox(frame, predictions)
            self.save_to_database(detected_objects)
            self.send_command_to_arduino(detected_objects)
            cv2.imshow("window", frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    def draw_bbox(self, img, p):
        detected_objects = []

        for label, bbox, probs in zip(*p):
            if probs < self._threshold:
                continue
            pt1 = (int(bbox[0]), int(bbox[1]))
            pt2 = (int(bbox[2]), int(bbox[3]))
            cv2.rectangle(img, pt1, pt2, (255, 0, 0), 3)
            cv2.putText(img, label, pt1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if label != 'person':
                detected_objects.append({'Product': label, 'Detection Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

        return detected_objects

    def save_to_database(self, detected_objects):
        try:
            for obj in detected_objects:
                product = obj['Product']
                detection_time = obj['Detection Time']
                if product in ['knife', 'scissors']:
                    category = 'Dangerous Object'
                else:
                    category = 'Safe Object'

                # Veritabanına ekle
                self._cursor.execute("INSERT INTO detected_objects (product, category, detection_time) VALUES (?, ?, ?)",
                                     (product, category, detection_time))
                self._conn.commit()
        except Exception as e:
            print("Hata oluştu:", e)

    def send_command_to_arduino(self, detected_objects):
        try:
            for obj in detected_objects:
                product = obj['Product']
                if product in ['knife', 'scissors']:
                    self._ser.write(f'{product}\n'.encode())
                    time.sleep(2)
                    self._ser.write(b'0\n')
        except Exception as e:
            print("Hata oluştu:", e)

    def check_rfid_commands(self):
        try:
            if self._rfid_ser.in_waiting > 0:
                command = self._rfid_ser.readline().decode().strip()
                if command == "start_ui":
                    self.start_user_interface()
                elif command == "stop_ui":
                    self.stop_user_interface()
        except Exception as e:
            print("Hata oluştu:", e)

    def start_user_interface(self):
        if self.user_interface_process is None:
            self.user_interface_process = subprocess.Popen(["python", "C://Users//ekino//Desktop//Capstone//sunum//UserInterfaceBG.py"])
            print("UserInterface is started!")

    def stop_user_interface(self):
        if self.user_interface_process is not None:
            self.user_interface_process.terminate()
            self.user_interface_process = None
            print("UserInterface is closed!")

def main():
    camera = LaptopCamera(0)
    detector = Detector()
    db_file = 'detected_objects_sqlite3.db'
    node = DetectorNode("detector_node", camera, detector, 0.85, db_file, 'COM9', 'COM12')
    node.run()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
