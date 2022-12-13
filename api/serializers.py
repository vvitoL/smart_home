from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Device, ExtraInfo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ExtraInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExtraInfo
        fields = ["consumption", 'kind']


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    extra_info = ExtraInfoSerializer(many=False)

    class Meta:
        model = Device
        fields = ['name', 'desc', 'state', 'id', 'last_mod', 'created', 'amount_changes', 'long_name', "extra_info"]


class DeviceMiniSerializer(serializers.HyperlinkedModelSerializer):
    extra_info = ExtraInfoSerializer(many=False)

    class Meta:
        model = Device
        fields = ['name', 'state', "extra_info"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
