from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks.models import Task
from tournaments.models import Tournament, TournamentLeaderboard
from tournaments.serializers import (
    TournamentSerializer,
    TournamentListSerializer,
    TournamentLeaderboardSerializer,
    TournamentJoinCompetitionSerializer,
    TournamentJoinCompetitionNestedSerializer,
    TournamentSubmitAnswerSerializer,
    TournamentUseTaskHintSerializer
)


class TournamentViewSet(ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()
    permission_classes_by_action = {
        'create': [IsAdminUser],
        'retrieve': [IsAdminUser],
        'update': [IsAdminUser],
        'list': [IsAuthenticated]
    }

    class Meta:
        model = Tournament

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return TournamentListSerializer

        return super().get_serializer_class()


class TournamentJoinCompetitionView(GenericAPIView):
    serializer_class = TournamentJoinCompetitionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Tournament.objects.all()
    lookup_url_kwarg = 'tournament_id'

    def post(self, request, *args, **kwargs):
        tournament = self.get_object()
        tournament.join(team=request.user)

        serializer = TournamentJoinCompetitionNestedSerializer(data={
            "tournament": tournament.id,
            "team": request.user.id,
        })
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TournamentSubmitAnswerView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TournamentSubmitAnswerSerializer
    queryset = Tournament.objects.all()
    lookup_url_kwarg = 'tournament_id'

    def post(self, request, *args, **kwargs):
        tournament = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = serializer.validated_data.get('task')
        serializer = self.get_serializer(tournament.submit_answer(
            team=request.user,
            task=task,
            answer=serializer.validated_data.get('answer')
        ))

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TournamentUseTaskHintView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TournamentUseTaskHintSerializer
    queryset = Tournament.objects.all()
    lookup_url_kwarg = 'tournament_id'

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            'task',
            in_=openapi.IN_QUERY,
            description='Task pk that needs to get a hint',
            type=openapi.TYPE_INTEGER)
    ])
    def get(self, request, *args, **kwargs):
        tournament = self.get_object()
        task = get_object_or_404(Task, pk=request.query_params.get('task'))

        serializer = self.get_serializer(data={
            'task': task.id,
            'hint': tournament.get_task_hint(task=task, team=request.user)
        })
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TournamentLeaderboardView(ListAPIView):
    serializer_class = TournamentLeaderboardSerializer
    ordering_fields = ('total_tasks_passed', 'total_penalty_time')
    lookup_url_kwarg = 'tournament_id'

    def get_queryset(self):
        return TournamentLeaderboard.objects.filter(
            tournament__id=self.kwargs.get(self.lookup_url_kwarg)
        ).order_by(*self.ordering_fields)
