from rest_framework import serializers

from tasks.serializers import TaskSerializer
from tournaments.models import (
    Tournament,
    TournamentRegistration,
    TournamentAttempt,
    TournamentLeaderboard
)


class TournamentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('id', 'tasks', 'start_timestamp', 'finish_timestamp')


class TournamentSerializer(TournamentBaseSerializer):
    pass


class TournamentListSerializer(TournamentBaseSerializer):
    tasks = TaskSerializer(read_only=True, many=True)


class TournamentJoinCompetitionSerializer(serializers.Serializer):
    pass


class TournamentJoinCompetitionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentRegistration
        fields = ('id', 'tournament', 'team')

        extra_kwargs = {
            'id': {'read_only': True},
        }


class TournamentSubmitAnswerSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(required=False)

    class Meta:
        model = TournamentAttempt
        fields = ('task', 'answer', 'success')

        extra_kwargs = {
            'task': {'write_only': True},
            'answer': {'write_only': True},
            'success': {'read_only': True},
        }


class TournamentLeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentLeaderboard
        fields = ('team', 'total_penalty_time')
