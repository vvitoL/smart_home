
from django.urls import include, path
from rest_framework import routers

from api import views
from tasks import modbus_read_loop

# add.delay(4, 4)

modbus_read_loop.delay()

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)
router.register("devices", views.DeviceViewSet)
router.register("sensors", views.SensorViewSet)
router.register("history", views.SensorHistoryViewSet)
router.register("owners", views.OwnerViewSet)


print('test')
urlpatterns = [
    path('', include(router.urls)),
]
