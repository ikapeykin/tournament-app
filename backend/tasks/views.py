from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    permission_classes_by_action = {
        'create': [IsAdminUser],
        'retrieve': [IsAdminUser],
        'update': [IsAdminUser],
        'list': [IsAuthenticated]
    }

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
