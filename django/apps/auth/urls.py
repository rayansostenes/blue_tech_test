from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView


app_name = 'my_auth'

urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token', TokenRefreshView.as_view(), name='token_refresh'),
]
