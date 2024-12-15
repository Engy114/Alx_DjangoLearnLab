from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Post
from accounts.serializers import PostSerializer


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
