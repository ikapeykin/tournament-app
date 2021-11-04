from django.test import TestCase

from tournaments.models import Tournament
from tasks.models import Task


class TournamentTest(TestCase):
    def setUp(self) -> None:
        Tournament.objects.create()
