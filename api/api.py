from rest_framework import routers

from api.views import MyUserViewSet, RunningGroupViewSet

router = routers.DefaultRouter()

router.register(r'users', MyUserViewSet)
router.register(r'groups', RunningGroupViewSet)
