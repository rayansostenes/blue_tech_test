from django.urls import path, include
from .views import PollModelViewSet
from rest_framework import routers

app_name = 'polls'

router = routers.DefaultRouter()
router.register('', PollModelViewSet, 'polls')

urlpatterns = [
    path('', include(router.urls)),
]
