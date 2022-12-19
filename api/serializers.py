from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Device, ExtraInfo, Sensor, SensorHistory, Owner


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ExtraInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExtraInfo
        fields = ["consumption", 'device_kind']


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    extra_info = ExtraInfoSerializer(many=False)

    class Meta:
        model = Device
        fields = ['name', 'desc', 'state', 'id', 'last_mod', 'created', 'long_name', "extra_info"]
        read_only_fields = ("extra_info",)


class DeviceMiniSerializer(serializers.HyperlinkedModelSerializer):
    extra_info = ExtraInfoSerializer(many=False)

    class Meta:
        model = Device
        fields = ['id', 'name', 'state', "extra_info"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class SensorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name']


class HistorySerializer(serializers.HyperlinkedModelSerializer):
    sensor = SensorSerializer(many=False)  # read_only=True)

    class Meta:
        model = SensorHistory
        fields = ['temperature', 'created', 'updated', 'sensor']


class HistoryMiniSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SensorHistory
        fields = ['temperature', 'created']


class SensorFullSerializer(serializers.HyperlinkedModelSerializer):
    histories = HistoryMiniSerializer(many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'histories']


class OwnerSerializer(serializers.HyperlinkedModelSerializer):
    devices = DeviceMiniSerializer(many=True, )
    sensors = SensorSerializer(many=True, )

    class Meta:
        model = Owner
        fields = ['id', 'name', 'surname', 'devices', 'sensors']

    def create(self, validated_data):
        devices = validated_data["devices"]
        sensors = validated_data["sensors"]
        del validated_data["devices"]
        del validated_data["sensors"]

        owner = Owner.objects.create(**validated_data)

        for device in devices:
            d = Device.objects.create(**device)
            owner.devices.add(d)

        for sensor in sensors:
            s = Sensor.objects.create(**sensor)
            owner.sensors.add(s)

        owner.save()

        return owner

