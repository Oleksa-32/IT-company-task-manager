from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views import generic

from task_manager.forms import WorkerSearchForm, WorkerCreationForm, WorkerPositionUpdateForm, TaskForm
from task_manager.models import Worker, Task, Position, TaskType


# Create your views here.

def index(request):
    return render(request, 'task_manager/index.html')


class WorkerListView(generic.ListView):
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


class WorkerDetailView(generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("position")
    template_name = "task_manager/worker_detail.html"
    context_object_name = "worker"


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    #success_url = reverse_lazy("task_manager:worker-list")
    def form_valid(self, form):
        worker = form.save(commit=False)
        worker.save()  # Save the Worker object
        form.save_m2m()  # Save the ManyToMany relationship (positions)
        return redirect('task_manager:worker-list')


# class WorkerPositionUpdateView(generic.UpdateView):
#     model = Worker
#     form_class = WorkerPositionUpdateForm
#     success_url = reverse_lazy("task_manager:worker-list")

class WorkerUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerPositionUpdateForm  # Or your specific update form
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task_manager:worker-list")


class PositionListView(generic.ListView):
    model = Position
    paginate_by = 5
    template_name = 'task_manager/position_list.html'
    context_object_name = 'position_list'

class PositionCreateView(generic.CreateView):
    model = Position
    template_name = 'task_manager/position_form.html'
    fields = ['name']
    success_url = reverse_lazy("task_manager:position-list")


class PositionDetailView(generic.DetailView):
    model = Position
    template_name = 'task_manager/position_detail.html'
    context_object_name = 'position'

    def get_context_data(self, **kwargs):
        # Get the default context data
        context = super().get_context_data(**kwargs)

        position = self.get_object()
        # context['workers'] = position.worker_set.all()
        # context['tasks'] = position.task_set.all()

        return context

class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy('task_manager:position-list')
    template_name = 'task_manager/position_confirm_delete.html'

class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = ['name']  # Include fields you want to edit
    template_name = 'task_manager/position_form.html'
    success_url = reverse_lazy('task_manager:position-list')


class TaskTypeListView(generic.ListView):
    model = TaskType
    paginate_by = 5
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type_list"

class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    template_name = "task_manager/task_type_detail.html"
    context_object_name = "task_type"

class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    fields = ["name"]
    success_url = reverse_lazy("task_manager:task-type-list")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")

class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    template_name = "task_manager/task_type_form.html"
    fields = ["name"]
    success_url = reverse_lazy("task_manager:task-type-list")


def toggle_task_assignment(request, worker_id, task_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    task = get_object_or_404(Task, pk=task_id)

    # Toggle the worker's assignment to the task
    if worker in task.assignees.all():
        task.assignees.remove(worker)
    else:
        task.assignees.add(worker)

    return redirect("task_manager:worker-detail", pk=worker.id)


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_manager/task_form.html'
    context_object_name = 'form'
    success_url = reverse_lazy('task_manager:task-list')


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = 'task_manager/task_detail.html'
    context_object_name = 'task'


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 10
    template_name = 'task_manager/task_list.html'
    context_object_name = 'task_list'


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('task_manager:task-list')


class TaskCompletionToggleView(generic.View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        return redirect('task_manager:task-detail', pk=task.pk)
