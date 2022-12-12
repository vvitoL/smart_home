
from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("groups", views.GroupViewSet)
router.register("devices", views.DeviceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
