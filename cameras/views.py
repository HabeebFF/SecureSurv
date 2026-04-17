from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Camera


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
        cameras = Camera.objects.values("id", "name", "location_name", "latitude", "longitude", "is_active")
        return Response(list(cameras), status=status.HTTP_200_OK)
