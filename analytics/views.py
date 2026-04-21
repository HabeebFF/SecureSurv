from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncHour
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


def login_page(request):
    return render(request, "auth/login.html")


def dashboard_page(request):
    return render(request, "dashboard/dashboard.html")


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from accounts.models import Person
        from cameras.models import Camera
        from recognition.models import DetectionEvent
        from alerts.models import Alert

        return Response({
            "total_cameras": Camera.objects.count(),
            "active_cameras": Camera.objects.filter(is_active=True).count(),
            "total_wanted_persons": Person.objects.filter(is_wanted=True).count(),
            "total_persons": Person.objects.count(),
            "total_detections": DetectionEvent.objects.count(),
            "total_alerts": Alert.objects.count(),
            "unread_alerts": Alert.objects.filter(is_read=False).count(),
        }, status=status.HTTP_200_OK)


class DetectionTrendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from recognition.models import DetectionEvent

        days = int(request.query_params.get("days", 30))
        since = timezone.now() - timedelta(days=days)

        data = (
            DetectionEvent.objects
            .filter(timestamp__gte=since)
            .annotate(date=TruncDate("timestamp"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        return Response(list(data), status=status.HTTP_200_OK)


class TopDetectedPersonsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from recognition.models import DetectionEvent

        limit = int(request.query_params.get("limit", 5))

        data = (
            DetectionEvent.objects
            .filter(person__isnull=False)
            .values("person__id", "person__name")
            .annotate(detections=Count("id"))
            .order_by("-detections")[:limit]
        )

        return Response([
            {
                "person_id": row["person__id"],
                "name": row["person__name"],
                "detections": row["detections"],
            }
            for row in data
        ], status=status.HTTP_200_OK)


class CameraActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from recognition.models import DetectionEvent

        data = (
            DetectionEvent.objects
            .values("camera__id", "camera__name", "camera__location_name")
            .annotate(detections=Count("id"))
            .order_by("-detections")
        )

        return Response([
            {
                "camera_id": row["camera__id"],
                "name": row["camera__name"],
                "location": row["camera__location_name"],
                "detections": row["detections"],
            }
            for row in data
        ], status=status.HTTP_200_OK)


class HourlyActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from recognition.models import DetectionEvent

        days = int(request.query_params.get("days", 7))
        since = timezone.now() - timedelta(days=days)

        data = (
            DetectionEvent.objects
            .filter(timestamp__gte=since)
            .annotate(hour=TruncHour("timestamp"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )

        return Response(list(data), status=status.HTTP_200_OK)
