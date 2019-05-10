from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response as HttpResponse, responses

from .models import Poll, Choice, Vote
from .serializers import PollSerializer, VoteSerializer


class OnlyAdminCanWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return permissions.IsAuthenticated().has_permission(request, view)
        return permissions.IsAdminUser().has_permission(request, view)


class PollModelViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all().prefetch_related('choices')
    permission_classes = [OnlyAdminCanWritePermission]

    @action(
        methods=['get'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def results(self, request, pk=None):
        poll = get_object_or_404(Poll, pk=pk)
        user = request.user
        if not user.is_staff and not poll.user_has_voted(user):
            raise PermissionDenied()

        return HttpResponse({
            str(id): num
            for id, num in poll.results().values_list('id', 'votes')
        })

    @action(
        methods=['get'],
        detail=True,
        permission_classes=[permissions.IsAdminUser],
    )
    def votes_timeseries(self, request, pk=None):
        if not request.user.is_staff:
            raise PermissionDenied()
        return HttpResponse(Vote.votes_per_hour(pk))
    
    @action(
       methods=['post'],
       detail=True,
       permission_classes=[permissions.IsAuthenticated] 
    )
    def vote(self, resquest, pk):
        HttpResponse({})