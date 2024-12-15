from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer

# Get the custom user model
User = get_user_model()


class RegisterView(APIView):
    """
    Handles user registration.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create authentication token for the new user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "User registered successfully", "token": token.key},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user login and returns authentication token.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=username, password=password)
        if user:
            # Create or retrieve token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    Allows users to view and update their profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch user details
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        # Update user profile
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(APIView):
    """
    Allows a user to follow another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        if target_user == request.user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.add(target_user)
        return Response(
            {"message": f"You are now following {target_user.username}"},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(APIView):
    """
    Allows a user to unfollow another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        if target_user == request.user:
            return Response(
                {"error": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.remove(target_user)
        return Response(
            {"message": f"You have unfollowed {target_user.username}"},
            status=status.HTTP_200_OK,
        )


class FollowingListView(APIView):
    """
    Displays the list of users the authenticated user is following.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following = request.user.following.all()
        data = [{"id": user.id, "username": user.username} for user in following]
        return Response(data, status=status.HTTP_200_OK)


class FollowersListView(APIView):
    """
    Displays the list of users following the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers = request.user.followers.all()
        data = [{"id": user.id, "username": user.username} for user in followers]
        return Response(data, status=status.HTTP_200_OK)
