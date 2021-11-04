from rest_framework_extensions.routers import ExtendedSimpleRouter

from tournaments.views import (
    TournamentViewSet,
    TournamentLeaderboardViewSet,
    TournamentSubmitAnswerViewSet,
    TournamentJoinCompetitionViewSet,
)

router: ExtendedSimpleRouter = ExtendedSimpleRouter()
tournaments_router = router.register('tournaments', TournamentViewSet, basename='api-tournaments')

tournaments_router.register(
    'leaderboard',
    TournamentLeaderboardViewSet,
    basename='api-tournaments-leaderboard',
    parents_query_lookups=['tournament']
)

tournaments_router.register(
    'join',
    TournamentJoinCompetitionViewSet,
    basename='api-tournaments-join',
    parents_query_lookups=['tournament']
)

tournaments_router.register(
    'submit',
    TournamentSubmitAnswerViewSet,
    basename='api-tournaments-submit',
    parents_query_lookups=['tournament']
)

urlpatterns: [] = router.urls
