from rest_framework import routers

from core.api.views import UserViewSet


router = routers.DefaultRouter()
router.register("profiles", UserViewSet)
urlpatterns = router.urls
