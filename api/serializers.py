from rest_framework import serializers

from racemate.models import MyUser, RunningGroup, PastTraining


class RunningGroupSerializer(serializers.HyperlinkedModelSerializer):
    admins = serializers.StringRelatedField(many=True)
    members = serializers.StringRelatedField(many=True)

    class Meta:
        model = RunningGroup
        fields = ('url', 'id', 'name', 'members', 'admins')


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    running_groups = serializers.PrimaryKeyRelatedField(queryset=RunningGroup.objects.all(), source='members',
                                                        many=True)

    class Meta:
        model = MyUser
        fields = ('url', 'id', 'username', 'running_groups')

    def create(self, validated_data):
        profile_data = validated_data.pop('running_groups')
        user = RunningGroup.objects.create(**validated_data)
        MyUser.objects.create(user=user, **profile_data)
        return user


class PastTrainingSerializer(serializers.HyperlinkedModelSerializer):
    time_total_in_sec = serializers.IntegerField(source='time_total')
    time_total_in_hms = serializers.ReadOnlyField(source='get_time_total_in_hms')
    distance_total_in_m = serializers.IntegerField(source='distance_total')

    class Meta:
        model = PastTraining
        fields = ('url', 'id', 'name', 'time_total_in_sec', 'time_total_in_hms', 'distance_total_in_m', 'date', 'user')

    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=255)
    # time_total = serializers.IntegerField()
    # distance_total = serializers.IntegerField()
    # date = serializers.DateTimeField()
    #
    # # user = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    #
    # def create(self, validated_data):
    #     """
    #     Create and return a new `PastTrening` instance, given the validated data.
    #     """
    #     return PastTraining.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `PastTrening` instance, given the validated data.
    #     """
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.time_total = validated_data.get('time_total', instance.time_total)
    #     instance.distance_total = validated_data.get('distance_total', instance.distance_total)
    #     instance.date = validated_data.get('date', instance.date)
    #     instance.save()
    #     return instance
