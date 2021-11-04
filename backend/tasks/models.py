from django.contrib.postgres.fields import ArrayField
from django.db import models


class Task(models.Model):
    name = models.TextField()
    description = models.TextField()
    hints = ArrayField(models.TextField(), size=3)
    x = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    y = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    answer = models.TextField()

    def compare_answer(self, user_answer: str) -> bool:
        return self.answer == user_answer

    def get_hint(self, hint_number: int) -> str:
        return self.hints[hint_number]
