
from rest_framework import serializers

from racemate.models import MyUser, RunningGroup


class RunningGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RunningGroup
        fields = ('url', 'id', 'name', 'members', 'admins')


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    running_groups = serializers.PrimaryKeyRelatedField(queryset=RunningGroup.objects.all(), source='members', many=True)

    class Meta:
        model = MyUser
        fields = ('url', 'id', 'username', 'running_groups')
        # member =


