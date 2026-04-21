import sys
import cv2
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Camera


def _open_capture(source):
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY] if sys.platform == "win32" else [cv2.CAP_ANY]
    for backend in backends:
        cap = cv2.VideoCapture(source, backend)
        if cap.isOpened():
            return cap
        cap.release()
    return None


def _frame_generator(source):
    cap = _open_capture(source)
    if cap is None:
        return
    try:
        for _ in range(30):
            cap.read()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n")
    finally:
        cap.release()


class CameraFeedView(APIView):
    permission_classes = []

    def get(self, request, camera_id):
        try:
            camera = Camera.objects.get(id=camera_id, is_active=True)
        except Camera.DoesNotExist:
            return Response({"error": "Camera not found."}, status=status.HTTP_404_NOT_FOUND)

        source = int(camera.stream_url) if camera.stream_url.isdigit() else (camera.stream_url or 0)
        return StreamingHttpResponse(
            _frame_generator(source),
            content_type="multipart/x-mixed-replace; boundary=frame",
        )


class RegisterCameraView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        name = request.data.get("name")
        location_name = request.data.get("location_name")
        latitude = request.data.get("latitude", 0.0)
        longitude = request.data.get("longitude", 0.0)
        stream_url = request.data.get("stream_url", "")

        if not name or not location_name:
            return Response(
                {"error": "name and location_name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        camera = Camera.objects.create(
            name=name,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            stream_url=stream_url,
            is_active=True,
        )

        return Response(
            {
                "message": "Camera registered successfully.",
                "id": camera.id,
                "name": camera.name,
                "location_name": camera.location_name,
            },
            status=status.HTTP_201_CREATED,
        )


class GetAllCamerasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cameras = Camera.objects.values("id", "name", "location_name", "latitude", "longitude", "is_active", "stream_url")
        return Response(list(cameras), status=status.HTTP_200_OK)


class UpdateCameraView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, camera_id):
        try:
            camera = Camera.objects.get(id=camera_id)
        except Camera.DoesNotExist:
            return Response({"error": "Camera not found."}, status=status.HTTP_404_NOT_FOUND)

        updatable = ["name", "location_name", "latitude", "longitude", "stream_url", "is_active"]
        for field in updatable:
            if field in request.data:
                setattr(camera, field, request.data[field])
        camera.save()

        return Response(
            {
                "message": "Camera updated successfully.",
                "id": camera.id,
                "name": camera.name,
                "stream_url": camera.stream_url,
                "is_active": camera.is_active,
            },
            status=status.HTTP_200_OK,
        )
