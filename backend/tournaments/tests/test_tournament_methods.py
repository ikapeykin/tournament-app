from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from tasks.models import Task
from teams.models import Team
from tournaments.models import Tournament


class TournamentTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        # А где фикстуры......
        self.tasks = [
            Task.objects.create(
                name=f'Test task {i}',
                description=f'Test task {i} description',
                hints=[f'hint {i}.1', f'hint {i}.2', f'hint {i}.3'],
                answer=f'{i}'
            ) for i in range(1, 6)
        ]
        map(lambda task: task.save(), self.tasks)

        self.tournament = Tournament.objects.create(
            name='Test tournament',
            start_timestamp=timezone.now(),
            finish_timestamp=timezone.now() + timezone.timedelta(hours=5)
        )
        self.tournament.tasks.set(self.tasks)
        self.tournament.save()

        # Вот бы сюда паттерн фабрику..............................
        self.user_with_permissions = Team.objects.create(
            email='super@admin.com',
            staff=True,
            admin=True
        )
        self.user_with_permissions.set_password('Test_Admin_Password123')
        self.user_with_permissions.save()

        self.user_without_permissions = Team.objects.create(
            email='super@user.com'
        )
        self.user_without_permissions.set_password('Test_User_Password123')
        self.user_without_permissions.save()

        self.admin_credentials = {
            'email': 'super@admin.com',
            'password': 'Test_Admin_Password123'
        }

        self.user_credentials = {
            'email': 'super@user.com',
            'password': 'Test_User_Password123'
        }

    def test_tournament_creating_with_permissions(self):
        self.client.login(**self.admin_credentials)
        api_url = reverse('api-tournaments-list')
        resp = self.client.post(api_url, {
            'tasks': [self.tasks[0].id, self.tasks[1].id],
            'start_timestamp': timezone.now(),
            'finish_timestamp': timezone.now() + timezone.timedelta(hours=5)
        }, follow=True)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_tournament_creating_without_permissions(self):
        self.client.login(**self.user_credentials)
        api_url = reverse('api-tournaments-list')
        resp = self.client.post(api_url, {
            'tasks': [self.tasks[0].id, self.tasks[1].id],
            'start_timestamp': timezone.now(),
            'finish_timestamp': timezone.now() + timezone.timedelta(hours=5)
        }, follow=True)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_tournament_join(self):
        self.client.login(**self.user_credentials)

        api_url = reverse('api-tournaments-join', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.post(api_url, {}, follow=True)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_tournament_submit_correct_answer(self):
        self.client.login(**self.user_credentials)

        # Join tournament first
        api_url = reverse('api-tournaments-join', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.post(api_url, {}, follow=True)

        api_url = reverse('api-tournaments-submit', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.post(api_url, {
            'task': self.tasks[0].id,
            'answer': self.tasks[0].answer
        })

        self.assertDictEqual(resp.data, {'success': True})

    def test_tournament_submit_incorrect_answer(self):
        self.client.login(**self.user_credentials)

        # Join tournament first
        api_url = reverse('api-tournaments-join', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.post(api_url, {}, follow=True)

        api_url = reverse('api-tournaments-submit', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.post(api_url, {
            'task': self.tasks[0].id,
            'answer': 'INCORRECT_ANSWER'
        })

        self.assertDictEqual(resp.data, {'success': False})

    def test_tournament_get_task_hint(self):
        self.client.login(**self.user_credentials)

        # Join tournament first
        api_url = reverse('api-tournaments-join', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.post(api_url, {}, follow=True)

        # Request task hint
        api_url = reverse('api-tournaments-hint', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.get(api_url, {'task': self.tasks[0].id})

        self.assertDictEqual(resp.data, {'task': self.tasks[0].id, 'hint': self.tasks[0].hints[0]})

    def test_tournament_leaderboard(self):
        """
        Здесь наверняка важно описать что вообще за ерунда происходит.
        Весь этот файл представляет из себя интеграционные тесты, нежели unit-тестирование.
        Я решил поступить так, чтобы показать какие умею писать тесты для продакшена. Очевидно,
        интеграционные тесты имеют не меньшую важность, чем unit-tests. Мы проверяем здесь больше работоспособность
        нашего бекенда, правильность сериализации/десиарилизации данных.

        Unit-tests реализованы для Task модели, т.к. там несколько важных для нашего приложения функций.

        Данный тест не отображает полную достоверность по leaderboard'у, но так как мы знаем как отыгрываем действия,
        можем убедиться что нужна команда соберет правильное место. Для такого leaderboard'а я бы еще написал unit-tests
        в отдельном файле, чтобы гарантировать его работоспособность на 99,99%
        """

        # Let's play all tournament. First team will be loser.
        # First team will be with user_credentials
        self.client.login(**self.user_credentials)

        # Join tournament
        api_url = reverse('api-tournaments-join', kwargs={'tournament_id': self.tournament.id})
        self.client.post(api_url, {}, follow=True)

        # Request first hint for first task
        api_url = reverse('api-tournaments-hint', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.get(api_url, {'task': self.tasks[0].id})

        # Request second hint for first task
        api_url = reverse('api-tournaments-hint', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.get(api_url, {'task': self.tasks[0].id})

        # Submit incorrect answer for the first task
        api_url = reverse('api-tournaments-submit', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.post(api_url, {
            'task': self.tasks[0].id,
            'answer': 'INCORRECT_ANSWER'
        })

        # Submit all tasks with correct answer
        api_url = reverse('api-tournaments-submit', kwargs={'tournament_id': self.tournament.id})

        for task in self.tasks:
            resp = self.client.post(api_url, {
                'task': task.id,
                'answer': task.answer
            })

        # Let's play for the second team, which will be with admin_credentials
        self.client.login(**self.admin_credentials)

        # Join tournament
        api_url = reverse('api-tournaments-join', kwargs={'tournament_id': self.tournament.id})
        self.client.post(api_url, {}, follow=True)

        # Submit all tasks with correct answer
        api_url = reverse('api-tournaments-submit', kwargs={'tournament_id': self.tournament.id})

        for task in self.tasks:
            resp = self.client.post(api_url, {
                'task': task.id,
                'answer': task.answer
            })

        api_url = reverse('api-tournaments-leaderboard', kwargs={'tournament_id': self.tournament.id})
        resp = self.client.get(api_url)

        self.assertEqual(resp.data[0]['team'], self.user_with_permissions.id)
        self.assertEqual(resp.data[0]['total_tasks_passed'], 5)
        self.assertEqual(resp.data[1]['team'], self.user_without_permissions.id)
        self.assertEqual(resp.data[1]['total_tasks_passed'], 5)
