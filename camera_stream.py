import time
import cv2
import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "your_token_here"       # paste your login token here
CAMERA_ID = 1                   # the id returned when you registered the camera
SCAN_INTERVAL = 3               # seconds between each scan

headers = {"Authorization": f"Token {TOKEN}"}


def scan_frame(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    response = requests.post(
        f"{BASE_URL}/api/recognition/scan/",
        headers=headers,
        files={"frame": ("frame.jpg", buffer.tobytes(), "image/jpeg")},
        data={"camera_id": CAMERA_ID},
    )
    result = response.json()
    if response.status_code == 201:
        for match in result.get("matches", []):
            print(f"[ALERT] {match['person']} detected — {match['confidence']}% confidence (alert #{match['alert_id']})")
    else:
        print(f"[INFO] {result.get('message', 'No response')}")


def main():
    cap = cv2.VideoCapture(0)   # 0 = default laptop camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera started. Scanning for wanted persons...")
    last_scan = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow("Surveillance Feed", frame)

        now = time.time()
        if now - last_scan >= SCAN_INTERVAL:
            scan_frame(frame)
            last_scan = now

        # press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
