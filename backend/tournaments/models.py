from django.db import models
from django.utils import timezone

from tasks.models import Task
from teams.models import Team
from tournaments.responses import (
    TournamentAlreadyJoined,
    TournamentNotAvailable,
    TournamentTeamDidNotJoin,
    TournamentTaskNotAvailable
)
from tournaments.constants import PENALTY_WITH_HINT, PENALTY_WITH_INCORRECT_ATTEMPT


class Tournament(models.Model):
    name = models.TextField()
    tasks = models.ManyToManyField(Task)
    start_timestamp = models.DateTimeField(blank=True)
    finish_timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name
    
    def count_penalty_time(self, hints_used, attempts_made):
        """
        Get the penalty time for a team.
        :param hints_used:
        :param attempts_made:
        :return:
        """
        return timezone.now().timestamp() - self.start_timestamp.timestamp() + \
               (hints_used * PENALTY_WITH_HINT) + (attempts_made * PENALTY_WITH_INCORRECT_ATTEMPT)
    
    def count_task_hint_number(self, team: Team, task: Task) -> int:
        """
        Get the number of hints a team has used for a task.
        :param team:
        :param task:
        :return:
        """
        return TournamentAttempt.objects.filter(tournament=self, team=team, task=task).count()

    def count_attempts_made(self, team: Team, task: Task) -> int:
        """
        Get the number of attempts a team has made to solve a task.
        :param team:
        :param task:
        :return:
        """
        return TournamentAttempt.objects.filter(tournament=self, team=team, task=task).count()
    
    def get_task_hint(self, team: Team, task: Task) -> str:
        """
        Get a hint for a team.
        :param team:
        :param task:
        :return:
        """
        if not self.is_joined(team):
            raise TournamentTeamDidNotJoin

        if not self.is_active():
            raise TournamentNotAvailable

        if task not in self.tasks.all():
            raise TournamentTaskNotAvailable

        hint = task.get_hint(hint_number=self.count_task_hint_number(team, task))
        TournamentHint.objects.create(tournament=self, team=team, task=task, used_hint=True)

        return hint

    def add_task_result(self, team: Team, task: Task, passed: bool, penalty_time: int):
        """
        Add a task result for a team.
        :param team:
        :param task:
        :param passed:
        :param penalty_time:
        :return:
        """
        if not TournamentLeaderboard.objects.filter(tournament=self, team=team).exists():
            TournamentLeaderboard.objects.create(tournament=self, team=team)

        team_leaderboard = TournamentLeaderboard.objects.get(tournament=self, team=team)
        team_leaderboard.add_task_result(task, passed, penalty_time)

    def get_registrations(self):
        """
        Get all registrations for a tournament.
        :return:
        """
        return TournamentRegistration.objects.filter(tournament=self)

    def is_active(self) -> bool:
        """
        Check if a tournament is active.
        :return:
        """
        # TODO: return self.finish_timestamp > timezone.now() > self.start_timestamp
        return timezone.now() < self.finish_timestamp

    def is_joined(self, team: Team) -> bool:
        """
        Check if a team is joined to a tournament.
        :param team:
        :return:
        """
        return TournamentRegistration.objects.filter(tournament=self, team=team).exists()

    def join(self, team: Team):
        """
        Join a team to a tournament.
        :param team:
        :return:
        """
        if not self.is_active():
            raise TournamentNotAvailable

        if self.is_joined(team):
            raise TournamentAlreadyJoined

        return TournamentRegistration.objects.create(tournament=self, team=team)

    def leave(self, team):
        """
        Leave a team from a tournament.
        :param team:
        :return:
        """
        return TournamentRegistration.objects.filter(tournament=self, team=team).delete()

    def submit_answer(self, team: Team, task: Task, answer: str):
        """
        Submit an answer to a task.
        :param team:
        :param answer:
        :param task:
        :return:
        """
        # TODO: Здесь закрался баг, нужно еще проверять начался ли турнир
        # TODO: Проверить сдана ли задача

        if not self.is_joined(team):
            raise TournamentTeamDidNotJoin

        if not self.is_active():
            raise TournamentNotAvailable

        if task not in self.tasks.all():
            raise TournamentTaskNotAvailable

        attempt_success: bool = task.compare_answer(answer)

        if attempt_success:
            hints_used: int = self.count_task_hint_number(team, task)
            attempts_made: int = self.count_attempts_made(team, task)
            penalty_time: int = self.count_penalty_time(hints_used, attempts_made)
            self.add_task_result(team=team, task=task, passed=True, penalty_time=penalty_time)

        return TournamentAttempt.objects.create(tournament=self, team=team, task=task, success=attempt_success)


class TournamentRegistration(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    registration_timestamp = models.DateTimeField(default=timezone.now)


class TournamentHint(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    used_hint = models.BooleanField()


class TournamentAttempt(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(verbose_name="Success of the task")


class TournamentTaskResult(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    passed = models.BooleanField(verbose_name="Passed")
    penalty_time = models.IntegerField(verbose_name="Penalty time")
    score = models.IntegerField(default=0)


class TournamentLeaderboard(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    results = models.ManyToManyField(TournamentTaskResult)
    total_penalty_time = models.IntegerField(default=0)
    total_tasks_passed = models.IntegerField(default=0)

    def add_task_result(self, task: Task, passed: bool, penalty_time: int):
        """
        Add a task result to the leaderboard.
        :param task:
        :param passed:
        :param penalty_time:
        :return:
        """
        if not passed:
            return

        self.total_penalty_time += penalty_time
        self.total_tasks_passed += 1
        self.results.add(TournamentTaskResult.objects.create(task=task, passed=passed, penalty_time=penalty_time))
