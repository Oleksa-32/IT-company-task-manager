from django.urls import path

from .forms import WorkerPositionUpdateForm
from .views import (
    index, WorkerListView, WorkerDetailView, WorkerCreateView, WorkerDeleteView,
    PositionListView, PositionCreateView, PositionDetailView, toggle_task_assignment, WorkerUpdateView,
    PositionDeleteView, PositionUpdateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
# path(
#         'tasks/<int:pk>/toggle-assignment/',
#         toggle_task_assignment,
#         name='toggle-task-assignment'
#     ),
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
    path('positions/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
    path('positions/', PositionListView.as_view(), name='position-list'),
    path('positions/create/', PositionCreateView.as_view(), name='position-create'),
    path('position/<int:pk>/delete/', PositionDeleteView.as_view(), name='position-delete'),
    path('position/<int:pk>/update/', PositionUpdateView.as_view(), name='position-update'),
    #path('task/<int:task_id>/toggle-position/<int:position_id>/', toggle_task_assignment, name='toggle-task-assignment'),
]

app_name = 'task_manager'
