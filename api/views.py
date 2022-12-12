from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from api.models import Device
from api.serializers import UserSerializer, GroupSerializer
from api.serializers import DeviceSerializer


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

    # def get_queryset(self):
    #     dev_enabled = Device.objects.filter(state=False)
    #     return dev_enabled

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
