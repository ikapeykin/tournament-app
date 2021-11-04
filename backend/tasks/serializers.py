from rest_framework import serializers

from tasks.models import Task


class TaskBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "name", "description", "x", "y", "hints", "answer")
        extra_kwargs = {
            "answer": {"write_only": True},
            "hints": {"write_only": True},
        }


class TaskSerializer(TaskBaseSerializer):
    pass
