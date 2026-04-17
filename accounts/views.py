from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import api_view

from .models import User as Admin, Person


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


class AddPersonView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        photo = request.FILES.get("photo")
        is_wanted = request.data.get("is_wanted", False)

        if not name or not photo:
            return Response(
                {"error": "name and photo are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        person = Person.objects.create(
            name=name,
            photo=photo,
            is_wanted=is_wanted,
            encoding=b"",
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
