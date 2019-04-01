# Create your views here.

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsOwnerOrReadOnly
from api.serializers import MyUserSerializer, RunningGroupSerializer, PastTrainingSerializer
from racemate.models import MyUser, RunningGroup, PastTraining


class MyUserViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """Serializer for MyUser Model"""
    permission_classes = (IsAuthenticatedOrReadOnly,)
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
    """Serializer for RunningGroup Model"""

    queryset = RunningGroup.objects.all()
    serializer_class = RunningGroupSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PastTrainingViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """Serializer for PastTraining Model"""
    permission_classes = (IsAuthenticated,)
    queryset = PastTraining.objects.all()
    serializer_class = PastTrainingSerializer
#
# class PastTrainingList(APIView):
#     """
#     List all past_trainings, or create a new past_training.
#     """
#
#     def get(self, request, format=None):
#         past_training = PastTraining.objects.all()
#         serializer = PastTrainingSerializer(past_training, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PastTrainingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PastTrainingDetail(APIView):
#     """
#     Retrieve, update or delete a past_training instance.
#     """
#
#     def get_object(self, pk):
#         try:
#             return PastTraining.objects.get(pk=pk)
#         except PastTraining.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         past_training = self.get_object(pk)
#         serializer = PastTrainingSerializer(past_training)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         past_training = self.get_object(pk)
#         serializer = PastTrainingSerializer(past_training, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         past_training = self.get_object(pk)
#         past_training.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
