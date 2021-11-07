from django.test import TestCase

from tasks.models import Task


class TaskMethodsTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Task Description',
            hints=['hint A', 'hint B', 'hint C'],
            answer='ABC',
            x=0.10000,
            y=0.10000,
        )

    def test_task_comparing_answer(self):
        self.assertEqual(self.task.compare_answer('CBA'), False)
        self.assertEqual(self.task.compare_answer('abc'), False)
        self.assertEqual(self.task.compare_answer('ABC'), True)

    def test_task_get_hint(self):
        self.assertEqual(self.task.get_hint(0), 'hint A')
        self.assertEqual(self.task.get_hint(1), 'hint B')
        self.assertEqual(self.task.get_hint(2), 'hint C')
