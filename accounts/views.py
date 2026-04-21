import pickle

import face_recognition
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import Person
from .models import User as Admin


class CreateAdminView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")
        email = request.data.get("email", "")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        if not username or not password or not role:
            return Response(
                {"error": "username, password and role are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_roles = ["admin", "security", "analyst"]
        if role not in valid_roles:
            return Response(
                {"error": f"role must be one of: {', '.join(valid_roles)}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Admin.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = Admin.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_staff=(role == "admin"),
        )
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "Account created successfully.",
                "username": user.username,
                "role": user.role,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "message": "Login successful.",
                "token": token.key,
                "username": user.username,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
def logout_view(request):
    request.auth.delete()
    return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)


class GetAllUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = Admin.objects.values("id", "username", "email", "first_name", "last_name", "role", "is_active")
        return Response(list(users), status=status.HTTP_200_OK)


class GetAllPersonsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        persons = Person.objects.values("id", "name", "is_wanted", "created_at", "photo")
        return Response(list(persons), status=status.HTTP_200_OK)


class ToggleWantedStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, person_id):
        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return Response({"error": "Person not found."}, status=status.HTTP_404_NOT_FOUND)

        person.is_wanted = not person.is_wanted
        person.save(update_fields=["is_wanted"])

        return Response(
            {
                "message": f"{'Marked as wanted' if person.is_wanted else 'Removed from wanted list'}.",
                "id": person.id,
                "name": person.name,
                "is_wanted": person.is_wanted,
            },
            status=status.HTTP_200_OK,
        )


class AddPersonView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        photo = request.FILES.get("photo")
        is_wanted = request.data.get("is_wanted", False)

        is_wanted = str(is_wanted).lower() in ["true", "1", "yes"]

        if not name or not photo:
            return Response(
                {"error": "name and photo are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        image = face_recognition.load_image_file(photo)
        encodings = face_recognition.face_encodings(image)

        if not encodings:
            return Response(
                {"error": "No face detected in the photo. Please use a clear face image."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        encoding = pickle.dumps(encodings[0])

        photo.seek(0)
        person = Person.objects.create(
            name=name,
            photo=photo,
            is_wanted=is_wanted,
            encoding=encoding,
        )

        return Response(
            {
                "message": "Person profile added successfully.",
                "id": person.id,
                "name": person.name,
                "is_wanted": person.is_wanted,
                "photo": request.build_absolute_uri(person.photo.url),
            },
            status=status.HTTP_201_CREATED,
        )
