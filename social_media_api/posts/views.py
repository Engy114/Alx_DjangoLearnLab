from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from accounts.serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CustomUser
from accounts.serializers import UserSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object
        return obj.user == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Set the user as the creator of the post
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Set the user as the creator of the comment
        post_id = self.request.data.get('post')
        serializer.save(user=self.request.user, post_id=post_id)

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch posts from users the current user is following
        followed_users = request.user.following.all()
        posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)