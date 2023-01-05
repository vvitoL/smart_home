import datetime
import os

from django.contrib.auth.models import User, Group
from pyModbusTCP.client import ModbusClient
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import Device, SensorHistory, Sensor, Owner
from api.serializers import UserSerializer, GroupSerializer, OwnerSerializer, \
    HistorySerializer, DeviceSerializer, DeviceMiniSerializer, SensorFullSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        kind = self.request.query_params.get('kind', None)
        if kind:
            devices = Device.objects.filter(extra_info__device_kind__iexact=kind)
        else:
            devices = Device.objects.all()
        return devices

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = DeviceMiniSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeviceSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.data.get('state', ''):
            dev_state = True
        else:
            dev_state = False
        device = Device.objects.create(
            name=request.data['name'],
            desc=request.data['desc'],
            state=dev_state,
            amount_changes=request.data['amount_changes']
        )
        serializer = DeviceSerializer(device, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        device = self.get_object()
        device.name = request.data['name']
        device.desc = request.data['desc']
        if request.data.get('state', ''):
            device.state = True
        else:
            device.state = False
        device.modbus_register = request.data['modbus_register']
        device.plc_register = request.data['plc_register']
        device.save()

        serializer = DeviceSerializer(device, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        device = self.get_object()
        device.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("Device deleted")

    @action(detail=True, methods=['GET'])
    def changestate(self, request, **kwargs):
        device = self.get_object()

        if device.extra_info.device_kind == "BU":
            ex_coil = device.modbus_register
            c = ModbusClient(host="192.168.69.9", auto_open=True, auto_close=True)
            modbus_device = c.read_coils(ex_coil, 1)

            if modbus_device:
                c.write_single_coil(ex_coil, not modbus_device.pop())

                if (state := c.read_coils(ex_coil, 1)) is not None:
                    device.state = state.pop()
                    device.last_mod = datetime.datetime.now(tz=datetime.timezone.utc)
                    device.amount_changes += 1
                    device.save()

                    serializer = DeviceSerializer(device, many=False)
                    return Response(serializer.data)

            return Response(data="PLC not connected. Check the network.", status=404)
        elif device.extra_info.device_kind == "TU":
            ip_adress = os.getenv("IP_ADRESS")
        return Response(data="Wrong Parameters", status=404)


    @action(detail=False, methods=['PUT'])
    def offall(self, request, **kwargs):
        devices = Device.objects.all()
        devices.update(state=False)

        serializer = DeviceSerializer(devices, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
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


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorFullSerializer


class SensorHistoryViewSet(viewsets.ModelViewSet):
    queryset = SensorHistory.objects.all()
    serializer_class = HistorySerializer

    def create(self, request, *args, **kwargs):
        history = SensorHistory.objects.create(
            temperature=request.data['temperature'],
            sensor_id=request.data['sensor_id'],
        )
        serializer = HistorySerializer(history, many=False)
        return Response(serializer.data)


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    # permission_classes = [permissions.IsAuthenticated]

