# Create your views here.
import django_filters
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from api.permissions import IsOwnerOrReadOnly, IsOwner
from api.serializers import MyUserSerializer, RunningGroupSerializer, PastTrainingSerializer
from racemate.models import MyUser, RunningGroup, PastTraining


class MyUserViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """View for MyUser Model
    - unlogged user can read only
    - user can modify/delete only himself"""
    permission_classes = [IsAuthenticated, ]
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def perform_create(self, serializer):
        serializer.save(admins=self.request.user)


class RunningGroupViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    """View for RunningGroup Model
    - unlogged user can read only
    - user can modify/delete only his/her groups"""

    queryset = RunningGroup.objects.all()
    serializer_class = RunningGroupSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PastTrainingViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    """View for PastTraining Model
    - only for logged user
    - user only can see his trainings"""
    queryset = PastTraining.objects.all()
    serializer_class = PastTrainingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = [IsOwner, ]

    def get_queryset(self):
        """
        This view should return a list of all past trainings
        for the currently authenticated user.
        """
        owner = self.request.user
        return PastTraining.objects.filter(user=owner)
