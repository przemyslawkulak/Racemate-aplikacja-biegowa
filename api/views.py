from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.serializers import MyUserSerializer, RunningGroupSerializer
from racemate.models import MyUser, RunningGroup


class MyUserViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """Serializer for MyUser Model"""
    permission_classes = (IsAuthenticated,)
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class RunningGroupViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """Serializer for RunningGroup Model"""
    permission_classes = (IsAuthenticated,)
    queryset = RunningGroup.objects.all()
    serializer_class = RunningGroupSerializer
