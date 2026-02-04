import sys
import cv2
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap


class SkyVIVRobotController(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Load UI
        uic.loadUi("controller.ui", self)

        # Allow keyboard focus
        self.setFocusPolicy(Qt.StrongFocus)

        # ---- State ----
        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_frame)

        self.current_cmd = "STOP"

        # ---- Signals ----
        self.btnConnect.clicked.connect(self.connect_robot)

        self.btnForward.clicked.connect(lambda: self.send_command("FORWARD"))
        self.btnBackward.clicked.connect(lambda: self.send_command("BACKWARD"))
        self.btnLeft.clicked.connect(lambda: self.send_command("LEFT"))
        self.btnRight.clicked.connect(lambda: self.send_command("RIGHT"))
        self.btnStop.clicked.connect(lambda: self.send_command("STOP"))

        self.cameraType.currentTextChanged.connect(self.update_camera_hint)
        self.update_camera_hint(self.cameraType.currentText())

    # -------------------------
    # Robot / Camera
    # -------------------------
    def connect_robot(self):
        ip = self.ipInput.text().strip()
        cam_type = self.cameraType.currentText()
        cam_source = self.cameraSource.text().strip()

        self.statusLabel.setText(f"Status: CONNECTED to {ip}")
        self.statusLabel.setStyleSheet("color: green; font-weight: bold;")

        self.open_camera(cam_type, cam_source)

    def open_camera(self, cam_type, source):
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None

        try:
            if cam_type == "OpenCV":
                self.cap = cv2.VideoCapture(int(source))
            else:
                self.cap = cv2.VideoCapture(source)

            if not self.cap.isOpened():
                raise RuntimeError("Camera open failed")

            self.timer.start(30)

        except (ValueError, RuntimeError) as exc:
            self.statusLabel.setText(f"Camera error: {exc}")
            self.statusLabel.setStyleSheet("color: red;")

    def read_frame(self):
        if not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w

        qimg = QImage(
            frame.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888,
        )

        self.videoLabel.setPixmap(QPixmap.fromImage(qimg))

    # -------------------------
    # Keyboard (WASD)
    # -------------------------
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        key_map = {
            Qt.Key_W: "FORWARD",
            Qt.Key_S: "BACKWARD",
            Qt.Key_A: "LEFT",
            Qt.Key_D: "RIGHT",
        }

        cmd = key_map.get(event.key())
        if cmd:
            self.send_command(cmd)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return

        # Stop when movement key released
        if event.key() in (Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D):
            self.send_command("STOP")

    # -------------------------
    # UI Helpers
    # -------------------------
    def update_camera_hint(self, cam_type):
        hints = {
            "UDP": "udp://@:5000",
            "OpenCV": "0 (webcam index)",
            "RTSP": "rtsp://user:pass@ip/stream",
        }
        self.labelCamHint.setText(hints.get(cam_type, ""))

    # -------------------------
    # Robot Commands
    # -------------------------
    def send_command(self, cmd):
        if cmd == self.current_cmd:
            return

        self.current_cmd = cmd
        print(f"Robot command: {cmd}")
        self.statusLabel.setText(f"Status: {cmd}")


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SkyVIVRobotController()
    window.show()
    sys.exit(app.exec_())
