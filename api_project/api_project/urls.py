from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('api/', include('api.urls')),  # Routes to `api` app's URLs
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Token authentication endpoint
]

