from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Alert


class GetAllAlertsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        alerts = Alert.objects.select_related("event__person", "event__camera").order_by("-created_at")

        data = [
            {
                "id": alert.id,
                "message": alert.message,
                "is_read": alert.is_read,
                "created_at": alert.created_at,
                "person": alert.event.person.name if alert.event.person else "Unknown",
                "camera": alert.event.camera.name,
                "confidence": alert.event.confidence,
                "detection_image": request.build_absolute_uri(alert.event.image.url) if alert.event.image else None,
            }
            for alert in alerts
        ]

        return Response(data, status=status.HTTP_200_OK)
