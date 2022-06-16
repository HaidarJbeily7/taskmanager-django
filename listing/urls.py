
# from rest_framework import routers
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('lists', views.ListViewSet, basename='lists')
router.register('tasks', views.TaskViewSet, basename='tasks')

domain_router = routers.NestedDefaultRouter(router, 'lists', lookup='list')
domain_router.register('tasks', views.ListTasksViewSet, basename='list-tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(domain_router.urls)),
]
