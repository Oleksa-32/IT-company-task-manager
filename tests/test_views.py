from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Worker, Task, Position, TaskType

WORKER_URL = reverse("task_manager:worker-list")
TASK_URL = reverse("task_manager:task-list")
POSITION_URL = reverse("task_manager:position-list")
TASK_TYPE_URL = reverse("task_manager:task-type-list")

class PublicTest(TestCase):
    def test_login_required_worker(self):
        res = self.client.get(WORKER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_task(self):
        res = self.client.get(TASK_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_position(self):
        res = self.client.get(POSITION_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_task_type(self):
        res = self.client.get(TASK_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )
        self.client.login(username="testuser", password="testpassword123")

    def test_retrieve_worker(self):
        Worker.objects.create(username="worker1")
        response = self.client.get(WORKER_URL)
        self.assertEqual(response.status_code, 200)
        workers = Worker.objects.all()
        self.assertEqual(
            list(workers),
            list(response.context["worker_list"])
        )
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_retrieve_task(self):
        Task.objects.create(name="Test Task", description="Test Description", deadline="2024-12-31", priority="High", task_type=TaskType.objects.create(name="Type1"))
        response = self.client.get(TASK_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.all()
        self.assertEqual(
            list(tasks),
            list(response.context["task_list"])
        )
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_retrieve_position(self):
        Position.objects.create(name="Manager")
        response = self.client.get(POSITION_URL)
        self.assertEqual(response.status_code, 200)
        positions = Position.objects.all()
        self.assertEqual(
            list(positions),
            list(response.context["position_list"])
        )
        self.assertTemplateUsed(response, "task_manager/position_list.html")

    def test_retrieve_task_type(self):
        TaskType.objects.create(name="Urgent")
        response = self.client.get(TASK_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        task_types = TaskType.objects.all()
        self.assertEqual(
            list(task_types),
            list(response.context["task_type_list"])
        )
        self.assertTemplateUsed(response, "task_manager/task_type_list.html")
