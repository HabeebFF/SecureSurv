import pickle

import face_recognition
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from accounts.models import Person
from alerts.models import Alert
from cameras.models import Camera
from .models import DetectionEvent


class ScanFrameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        camera_id = request.data.get("camera_id")
        frame = request.FILES.get("frame")

        if not camera_id or not frame:
            return Response(
                {"error": "camera_id and frame are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            camera = Camera.objects.get(id=camera_id, is_active=True)
        except Camera.DoesNotExist:
            return Response(
                {"error": "Camera not found or inactive."},
                status=status.HTTP_404_NOT_FOUND,
            )

        image = face_recognition.load_image_file(frame)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        if not face_encodings:
            return Response({"message": "No faces detected in frame."}, status=status.HTTP_200_OK)

        wanted_persons = Person.objects.filter(is_wanted=True).exclude(encoding=b"")

        if not wanted_persons.exists():
            return Response({"message": "No wanted persons in database."}, status=status.HTTP_200_OK)

        known_encodings = []
        persons_list = []
        for person in wanted_persons:
            try:
                known_encodings.append(pickle.loads(bytes(person.encoding)))
                persons_list.append(person)
            except Exception:
                continue

        matches_found = []

        for face_encoding in face_encodings:
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            for idx, (distance, person) in enumerate(zip(distances, persons_list)):
                if distance <= 0.5:
                    confidence = round((1 - distance) * 100, 2)
                    frame.seek(0)
                    event = DetectionEvent.objects.create(
                        person=person,
                        camera=camera,
                        confidence=confidence,
                        image=frame,
                    )
                    alert = Alert.objects.create(
                        event=event,
                        message=f"Wanted person '{person.name}' detected by camera '{camera.name}' with {confidence}% confidence.",
                    )
                    matches_found.append({
                        "person": person.name,
                        "confidence": confidence,
                        "alert_id": alert.id,
                    })

        if matches_found:
            return Response(
                {"message": "Wanted person(s) detected.", "matches": matches_found},
                status=status.HTTP_201_CREATED,
            )

        return Response({"message": "No matches found."}, status=status.HTTP_200_OK)
