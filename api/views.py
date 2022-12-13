from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Device
from api.serializers import UserSerializer, GroupSerializer
from api.serializers import DeviceSerializer, DeviceMiniSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # dev_enabled = Device.objects.filter(state=False)
        dev_enabled = Device.objects.all()
        return dev_enabled

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = DeviceMiniSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeviceSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        device = Device.objects.create(
            name=request.data['name'],
            desc=request.data['desc'],
            state=request.data['state']
        )
        serializer = DeviceSerializer(device, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        device = self.get_object()
        device.name = request.data['name']
        device.state = request.data['state']
        device.desc = request.data['desc']
        device.save()

        serializer = DeviceSerializer(device, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        device = self.get_object()
        device.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Device deleted")

    @action(detail=True, methods=['PUT'])
    def changestate(self, request, **kwargs):
        device = self.get_object()
        if not device.state:
            device.state = True
        else:
            device.state = False
        device.save()

        serializer = DeviceSerializer(device, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def offall(self, request, **kwargs):
        devices = Device.objects.all()
        devices.update(state=False)

        serializer = DeviceSerializer(devices, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def onall(self, request, **kwargs):
        devices = Device.objects.all()
        devices.update(state=True)

        serializer = DeviceSerializer(devices, many=False)
        return Response(serializer.data)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
