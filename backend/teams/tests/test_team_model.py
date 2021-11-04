from django.test import TestCase

from teams.models import Team


class TeamTest(TestCase):
    def setUp(self) -> None:
        Team.objects.create(email='test4@team1.com', password='!en1k3p28HNIDSA')
        Team.objects.create(email='test5@team2.com', password='!en1HNIDSA8h2bri2u3')

    def test_username(self) -> None:
        test1 = Team.objects.get(email='test4@team1.com')
        test2 = Team.objects.get(email='test5@team2.com')
        self.assertEqual(test1.get_username(), 'test4@team1.com')
        self.assertEqual(test2.get_username(), 'test5@team2.com')

    def test_team_name(self) -> None:
        test1 = Team.objects.get(email='test4@team1.com')
        test1.email = 'Unlimited blade works'
        test2 = Team.objects.get(email='test5@team2.com')
        test2.email = 'Gunblades are cool!'
        self.assertEqual(test1.email, 'Unlimited blade works')
        self.assertEqual(test2.email, 'Gunblades are cool!')

    def test_change_password(self) -> None:
        test1 = Team.objects.get(email='test4@team1.com')
        test2 = Team.objects.get(email='test5@team2.com')
        pwd1 = 'monkeyDonkey007#$'
        pwd2 = 'OliverKant(3141++'
        self.assertEqual(test1.set_password(pwd1), None)
        self.assertEqual(test2.set_password(pwd2), None)

    def test_create_team(self) -> None:
        test3 = Team.objects.create(email='NewTeam', password='Omae@wa@mou$in')
        self.assertEqual(test3.email, 'NewTeam')
