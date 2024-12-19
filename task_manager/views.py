from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views import generic

from task_manager.forms import (WorkerSearchForm, WorkerCreationForm,
                            WorkerPositionUpdateForm, TaskForm, TaskSearchForm,
                            PositionSearchForm, TaskTypeSearchForm)
from task_manager.models import Worker, Task, Position, TaskType


@login_required
def index(request):
    return render(request, "task_manager/index.html")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker  # Ensures a default queryset is used
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = WorkerSearchForm(self.request.GET)
        queryset = Worker.objects.all()  # Ensures queryset is defined
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("position")
    template_name = "task_manager/worker_detail.html"
    context_object_name = "worker"


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5
    template_name = "task_manager/position_list.html"
    context_object_name = "position_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            return queryset.filter(name__icontains=name)
        return queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    template_name = "task_manager/position_form.html"
    fields = ["name"]
    success_url = reverse_lazy("task_manager:position-list")


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    template_name = "task_manager/position_detail.html"
    context_object_name = "position"


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task_manager:position-list")
    template_name = "task_manager/position_confirm_delete.html"

class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = ["name"]
    template_name = "task_manager/position_form.html"
    success_url = reverse_lazy("task_manager:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskTypeSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            return queryset.filter(name__icontains=name)
        return queryset

class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    template_name = "task_manager/task_type_detail.html"
    context_object_name = "task_type"

class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    fields = ["name"]
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")

class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    fields = ["name"]
    success_url = reverse_lazy("task_manager:task-type-list")


@login_required
def toggle_task_assignment(request, worker_id, task_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    task = get_object_or_404(Task, pk=task_id)

    # Toggle the worker"s assignment to the task
    if worker in task.assignees.all():
        task.assignees.remove(worker)
    else:
        task.assignees.add(worker)

    return redirect("task_manager:worker-detail", pk=worker.id)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_manager/task_form.html"
    context_object_name = "form"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"
    context_object_name = "task"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            return queryset.filter(name__icontains=name)
        return queryset


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class TaskCompletionToggleView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return redirect("task_manager:task-detail", pk=task.pk)
