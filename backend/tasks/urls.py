from rest_framework import routers

from tasks.views import TaskViewSet

router = routers.DefaultRouter()
tasks_router = router.register('tasks', TaskViewSet, basename='api-tasks')

urlpatterns: [] = router.urls
