from django.urls import path

from .forms import WorkerPositionUpdateForm
from .views import (
    index, WorkerListView, WorkerDetailView, WorkerCreateView, WorkerDeleteView,
    PositionListView, PositionCreateView, PositionDetailView, toggle_task_assignment, WorkerUpdateView,
    PositionDeleteView, PositionUpdateView, TaskTypeCreateView, TaskTypeDetailView, TaskTypeDeleteView,
    TaskTypeListView, TaskTypeUpdateView, TaskDetailView, TaskUpdateView, TaskCompletionToggleView, TaskListView,
    TaskCreateView, TaskDeleteView,
)

urlpatterns = [

    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),

    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path(
        "workers/<int:worker_id>/tasks/<int:task_id>/toggle-assignment/",
        toggle_task_assignment,
        name="toggle-task-assignment",
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
    path("positions/<int:pk>/", PositionDetailView.as_view(), name="position-detail"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("position/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
    path("position/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    #path("task/<int:task_id>/toggle-position/<int:position_id>/", toggle_task_assignment, name="toggle-task-assignment"),

    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/", TaskTypeDetailView.as_view(), name="task-type-detail"),
    path("task-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("task/create/", TaskCreateView.as_view(), name="task-create"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/<int:pk>/toggle-completion/", TaskCompletionToggleView.as_view(), name="task-completion-toggle"),
]

app_name = "task_manager"
