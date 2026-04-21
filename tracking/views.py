from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import UserLocation


class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if latitude is None or longitude is None:
            return Response(
                {"error": "latitude and longitude are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        location, _ = UserLocation.objects.update_or_create(
            user=request.user,
            defaults={
                "latitude": latitude,
                "longitude": longitude,
                "tracking_enabled": True,
            },
        )

        return Response(
            {"message": "Location updated.", "latitude": location.latitude, "longitude": location.longitude},
            status=status.HTTP_200_OK,
        )


class ToggleTrackingView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        location, _ = UserLocation.objects.get_or_create(
            user=request.user,
            defaults={"latitude": 0.0, "longitude": 0.0, "tracking_enabled": False},
        )
        location.tracking_enabled = not location.tracking_enabled
        location.save(update_fields=["tracking_enabled"])

        return Response(
            {
                "message": f"Tracking {'enabled' if location.tracking_enabled else 'disabled'}.",
                "tracking_enabled": location.tracking_enabled,
            },
            status=status.HTTP_200_OK,
        )


class ActiveLocationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = UserLocation.objects.filter(tracking_enabled=True).select_related("user")

        return Response(
            [
                {
                    "user_id": loc.user.id,
                    "username": loc.user.username,
                    "full_name": f"{loc.user.first_name} {loc.user.last_name}".strip(),
                    "role": loc.user.role,
                    "latitude": loc.latitude,
                    "longitude": loc.longitude,
                    "last_updated": loc.last_updated,
                }
                for loc in locations
            ],
            status=status.HTTP_200_OK,
        )
