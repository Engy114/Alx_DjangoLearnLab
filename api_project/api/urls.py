from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),  # Includes URLs from the `api` app
]