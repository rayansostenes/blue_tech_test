from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import TokenSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenSerializer
