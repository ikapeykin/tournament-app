from django.contrib.auth.backends import BaseBackend

from teams.models import Team


class EmailBackend(BaseBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = Team.objects.get(email=email)
        except Team.DoesNotExist:
            return None
        return user
