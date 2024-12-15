from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from accounts.serializers import PostSerializer, CommentSerializer
from accounts.views import permissions,IsAuthenticated

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
