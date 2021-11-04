from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from tasks.models import Task
from tasks.serializers import TaskSerializer


# TODO: Implement permissions for POST/DELETE methods stuff only
class TaskViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
