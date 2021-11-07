from django.contrib import admin

from tournaments.models import (
    Tournament,
    TournamentAttempt,
    TournamentLeaderboard,
    TournamentHint,
    TournamentRegistration,
    TournamentTaskResult
)

admin.site.register(Tournament)
admin.site.register(TournamentAttempt)
admin.site.register(TournamentLeaderboard)
admin.site.register(TournamentHint)
admin.site.register(TournamentRegistration)
admin.site.register(TournamentTaskResult)
