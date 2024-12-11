from django.shortcuts import render
from rest_framework.views import APIView
from accounts.views import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get posts from users the current user is following
        following_users = request.user.following.all()
        posts = Post.objects.filter(user__in=following_users).order_by('-created_at')

        # Serialize and return posts
        feed = [{"user": post.user.username, "content": post.content, "created_at": post.created_at} for post in posts]
        return Response(feed, status=status.HTTP_200_OK)

