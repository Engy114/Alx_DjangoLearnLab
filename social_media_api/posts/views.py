from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from accounts.serializers import PostSerializer, CommentSerializer
from notifications.models import Notification
from accounts.views import permissions,IsAuthenticated
from accounts.views import generics

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the current user as the post author
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the current user as the comment author
        serializer.save(author=self.request.user)


class FeedView(APIView):
    """
    Returns posts from users that the authenticated user is following.
    Posts are ordered by creation date, showing the most recent first.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve users the current user is following
        following_users = request.user.following.all()

        # Filter posts by users the current user follows and order them by creation date
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Serialize and return the posts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikePostView(APIView):
    """
    Allows an authenticated user to like a post and creates a notification.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Retrieve the post or return 404
        post = get_object_or_404(Post, pk=pk)
        # Check if the like already exists
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # Create notification for the post author
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post,
            )
            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(APIView):
    """
    Allows an authenticated user to unlike a post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Retrieve the post or return 404
        post = get_object_or_404(Post, pk=pk)
        post = generics.get_object_or_404(Post, pk=pk)

        # Find and delete the like if it exists
        like = Like.objects.filter(user=request.user, post=post).first()
        if like:
            like.delete()
            return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
