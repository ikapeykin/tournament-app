from django.conf.urls import url
from rest_framework import routers

from tournaments.views import (
    TournamentViewSet,
    TournamentLeaderboardView,
    TournamentSubmitAnswerView,
    TournamentJoinCompetitionView,
    TournamentUseTaskHintView
)

router = routers.DefaultRouter()
router.register(r"tournaments", TournamentViewSet, basename='api-tournaments')

urlpatterns: [] = [
    *router.urls,

    url(
        r'^tournaments/(?P<tournament_id>\d+)/join',
        TournamentJoinCompetitionView.as_view(),
        name='api-tournaments-join'
    ),
    url(
        r'^tournaments/(?P<tournament_id>\d+)/leaderboard',
        TournamentLeaderboardView.as_view(),
        name='api-tournaments-leaderboard'),
    url(
        r'^tournaments/(?P<tournament_id>\d+)/submit',
        TournamentSubmitAnswerView.as_view(),
        name='api-tournaments-submit'),
    url(
        r'^tournaments/(?P<tournament_id>\d+)/hint',
        TournamentUseTaskHintView.as_view(),
        name='api-tournaments-hint'),
]
