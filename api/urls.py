from django.urls import include, path
from rest_framework import routers
from dotenv import load_dotenv

from api import views
from tasks import modbus_read_loop

load_dotenv()
modbus_read_loop.delay()

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)
router.register("devices", views.DeviceViewSet)
router.register("sensors", views.SensorViewSet)
router.register("history", views.SensorHistoryViewSet)
router.register("owners", views.OwnerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
