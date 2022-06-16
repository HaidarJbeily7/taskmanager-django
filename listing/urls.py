
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('lists', views.ListViewSet, basename='lists')

urlpatterns = router.urls
