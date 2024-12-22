from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from task_manager.models import Position, TaskType, Worker, Task

class TestModels(TestCase):
    def test_position_str(self):
        position = Position.objects.create(name="Manager")
        self.assertEqual(str(position), position.name)

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Development")
        self.assertEqual(str(task_type), task_type.name)

    def test_worker_str(self):
        username = "worker1"
        first_name = "John"
        last_name = "Smith"
        password = "password123"
        worker = get_user_model().objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        self.assertEqual(str(worker), f"{username}")

    def test_task_str(self):
        task_type = TaskType.objects.create(name="Testing")
        task = Task.objects.create(
            name="Task 1",
            description="This is a test task.",
            deadline=date(2024, 12, 31),
            is_completed=False,
            priority="High",
            task_type=task_type,
        )
        self.assertEqual(str(task), task.name)
