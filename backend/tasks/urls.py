from rest_framework_extensions.routers import ExtendedSimpleRouter

from tasks.views import TaskViewSet

router: ExtendedSimpleRouter = ExtendedSimpleRouter()
tasks_router = router.register('tasks', TaskViewSet, basename='api-tasks')

urlpatterns: [] = router.urls
