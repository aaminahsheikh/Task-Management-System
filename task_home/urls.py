from django.urls import path, include
from rest_framework.routers import DefaultRouter

from task_home.views import home, UserViewSet, TaskViewSet

urlpatterns = [
    path("", home, name="home"),
]

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register('tasks', TaskViewSet, basename='tasks')
urlpatterns = router.urls

