from django.test import TestCase
from django.urls import reverse_lazy


class FormsTests(TestCase):
    def test_worker_search_form(self):
        data = {
            "username": "test_username",
        }
        response = self.client.get(
            reverse_lazy("task_manager:worker-list"),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")

    def test_task_search_form(self):
        data = {
            "name": "test_task_name",
        }
        response = self.client.get(
            reverse_lazy("task_manager:task-list"),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")

    def test_position_search_form(self):
        data = {
            "name": "test_position_name",
        }
        response = self.client.get(
            reverse_lazy("task_manager:position-list"),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")

    def test_task_type_search_form(self):
        data = {
            "name": "test_task_type_name",
        }
        response = self.client.get(
            reverse_lazy("task_manager:task-type-list"),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")
