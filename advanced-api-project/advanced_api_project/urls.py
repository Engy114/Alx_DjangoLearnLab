from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('api/', include('api.urls')),  # Include URLs from the `api` app
]

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('api/', include('api.urls')),  # Include URLs from the `api` app
]
