from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from teams.models import Team
from tournaments.models import Tournament, TournamentLeaderboard
from tournaments.serializers import (
    TournamentSerializer,
    TournamentListSerializer,
    TournamentLeaderboardSerializer,
    TournamentJoinCompetitionSerializer,
    TournamentJoinCompetitionNestedSerializer,
    TournamentSubmitAnswerSerializer,
)


class TournamentViewSet(ModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()

    class Meta:
        model = Tournament

    def get_serializer_class(self):
        if self.action in ["retrieve"]:
            return TournamentListSerializer

        return super().get_serializer_class()


class TournamentJoinCompetitionViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TournamentJoinCompetitionSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_field = 'parent_lookup_tournament'

    def create(self, request, *args, **kwargs):
        tournament = get_object_or_404(Tournament, pk=kwargs.get(self.lookup_url_field))
        team = get_object_or_404(Team, email=request.user)

        tournament.join(team=team)

        serializer = TournamentJoinCompetitionNestedSerializer(data={
            "tournament": tournament.id,
            "team": team.id,
        })

        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TournamentSubmitAnswerViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TournamentSubmitAnswerSerializer
    lookup_url_field = 'parent_lookup_tournament'
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tournament = get_object_or_404(Tournament, pk=kwargs.get(self.lookup_url_field))
        team = get_object_or_404(Team, email=request.user)
        task = serializer.validated_data.get('task')

        serializer = self.get_serializer(tournament.submit_answer(
            team=team,
            task=task,
            answer=serializer.validated_data.get('answer')
        ))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TournamentLeaderboardViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = TournamentLeaderboardSerializer
    queryset = TournamentLeaderboard.objects.all()
