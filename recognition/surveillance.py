import pickle
import threading
import time

import cv2
import face_recognition
from django.core.files.base import ContentFile
from django.utils import timezone

SCAN_INTERVAL = 3
TOLERANCE = 0.5
ENCODINGS_RELOAD = 30


def _load_wanted_persons():
    from accounts.models import Person
    result = []
    for person in Person.objects.filter(is_wanted=True).exclude(encoding=b""):
        try:
            result.append((person, pickle.loads(bytes(person.encoding))))
        except Exception:
            continue
    return result


def _resolve_stream_source(url):
    if not url:
        return 0
    if "youtube.com" in url or "youtu.be" in url:
        try:
            import yt_dlp
            ydl_opts = {"quiet": True, "format": "best[ext=mp4]/best"}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats") or []
                direct_url = info.get("url") or (formats[-1].get("url") if formats else None)
                if direct_url:
                    print(f"[SURVEILLANCE] Resolved YouTube URL for '{url}'")
                    return direct_url
        except Exception as e:
            print(f"[SURVEILLANCE] yt-dlp error: {e}")
    return url


def _watch_camera(camera, stop_event):
    source = _resolve_stream_source(camera.stream_url)
    print(f"[SURVEILLANCE] Started — '{camera.name}' (source: {source})")

    cap = cv2.VideoCapture(source)
    known_persons = _load_wanted_persons()
    last_scan = 0
    last_reload = time.time()

    while not stop_event.is_set():
        if not cap.isOpened():
            cap = cv2.VideoCapture(source)
            time.sleep(2)
            continue

        ret, frame = cap.read()
        if not ret:
            time.sleep(2)
            cap.release()
            cap = cv2.VideoCapture(source)
            continue

        now = time.time()

        if now - last_reload >= ENCODINGS_RELOAD:
            known_persons = _load_wanted_persons()
            last_reload = now

        if now - last_scan >= SCAN_INTERVAL:
            _scan_frame(frame, camera, known_persons)
            last_scan = now

    cap.release()
    print(f"[SURVEILLANCE] Stopped — '{camera.name}'")


def _scan_frame(frame, camera, known_persons):
    if not known_persons:
        return

    from alerts.models import Alert
    from recognition.models import DetectionEvent

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    if not encodings:
        return

    known_encodings = [enc for _, enc in known_persons]
    persons_list = [p for p, _ in known_persons]

    for face_enc in encodings:
        distances = face_recognition.face_distance(known_encodings, face_enc)
        for distance, person in zip(distances, persons_list):
            if distance <= TOLERANCE:
                confidence = round((1 - distance) * 100, 2)
                _, buf = cv2.imencode(".jpg", frame)
                image_file = ContentFile(buf.tobytes(), name=f"det_{timezone.now().timestamp()}.jpg")
                event = DetectionEvent.objects.create(
                    person=person,
                    camera=camera,
                    confidence=confidence,
                    image=image_file,
                )
                Alert.objects.create(
                    event=event,
                    message=f"Wanted person '{person.name}' detected by '{camera.name}' with {confidence}% confidence.",
                )
                print(f"[ALERT] {person.name} on '{camera.name}' — {confidence}%")


class SurveillanceManager:
    def __init__(self):
        self._threads = {}      # camera_id -> Thread
        self._stop_events = {}  # camera_id -> Event
        self._lock = threading.Lock()

    @property
    def is_running(self):
        with self._lock:
            return any(t.is_alive() for t in self._threads.values())

    def start(self):
        from cameras.models import Camera
        cameras = Camera.objects.filter(is_active=True)
        for camera in cameras:
            self._start_camera(camera)

    def stop(self):
        with self._lock:
            for stop_event in self._stop_events.values():
                stop_event.set()
            self._threads.clear()
            self._stop_events.clear()
        print("[SURVEILLANCE] All cameras stopped.")

    def _start_camera(self, camera):
        with self._lock:
            existing = self._threads.get(camera.id)
            if existing and existing.is_alive():
                return
            stop_event = threading.Event()
            t = threading.Thread(
                target=_watch_camera,
                args=(camera, stop_event),
                daemon=True,
                name=f"camera-{camera.id}",
            )
            self._threads[camera.id] = t
            self._stop_events[camera.id] = stop_event
            t.start()


manager = SurveillanceManager()
