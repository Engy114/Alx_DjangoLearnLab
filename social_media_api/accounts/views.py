from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from .models import permission,IsAuthenticated

# Get the custom user model
CustomUser = get_user_model()
class ProfileView(APIView):
    """
    Allows users to view and update their profile.
    """
    permission_classes = [permission.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RegisterView(generics.GenericAPIView):
    """
    Handles user registration.
    """
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "User registered successfully", "token": token.key},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """
    Handles user login and returns authentication token.
    """
    serializer_class = UserSerializer

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
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(generics.GenericAPIView):
    """
    Allows a user to follow another user.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)
        return Response(
            {"message": f"You are now following {target_user.username}"},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(generics.GenericAPIView):
    """
    Allows a user to unfollow another user.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target_user)
        return Response(
            {"message": f"You have unfollowed {target_user.username}"},
            status=status.HTTP_200_OK,
        )


class FollowingListView(generics.GenericAPIView):
    """
    Displays the list of users the authenticated user is following.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following = request.user.following.all()
        data = [{"id": user.id, "username": user.username} for user in following]
        return Response(data, status=status.HTTP_200_OK)


class FollowersListView(generics.GenericAPIView):
    """
    Displays the list of users following the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        followers = request.user.followers.all()
        data = [{"id": user.id, "username": user.username} for user in followers]
        return Response(data, status=status.HTTP_200_OK)
