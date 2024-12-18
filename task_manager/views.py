from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DeleteView, UpdateView

from task_manager.forms import WorkerSearchForm, WorkerCreationForm, WorkerPositionUpdateForm
from task_manager.models import Worker, Task, Position


# Create your views here.

def index(request):
    return render(request, 'task_manager/index.html')


class WorkerListView(generic.ListView):
    model = Worker  # Ensures a default queryset is used
    paginate_by = 5

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
    template_name = 'task_manager/position_list.html'
    context_object_name = 'position_list'

class PositionCreateView(generic.CreateView):
    model = Position
    template_name = 'task_manager/position_form.html'
    fields = ['name']  # Assuming "name" is the only field in the Position model
    success_url = reverse_lazy("task_manager:worker-list")


class PositionDetailView(generic.DetailView):
    model = Position
    template_name = 'task_manager/position_detail.html'  # Path to the template
    context_object_name = 'position'  # Name to reference the position object in the template

    def get_context_data(self, **kwargs):
        # Get the default context data
        context = super().get_context_data(**kwargs)

        # Fetch the related workers and tasks associated with the position
        position = self.get_object()  # This is the Position object from the URL
        # context['workers'] = position.worker_set.all()  # Get workers assigned to this position
        # context['tasks'] = position.task_set.all()  # Get tasks assigned to this position

        return context

class PositionDeleteView(DeleteView):
    model = Position
    success_url = reverse_lazy('task_manager:position-list')  # Redirect to a list of positions
    template_name = 'task_manager/position_confirm_delete.html'

class PositionUpdateView(UpdateView):
    model = Position
    fields = ['name']  # Include fields you want to edit
    template_name = 'task_manager/position_form.html'
    success_url = reverse_lazy('task_manager:position-list')  # Redirect after update


def toggle_task_assignment(request, worker_id, task_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    task = get_object_or_404(Task, pk=task_id)

    # Toggle the worker's assignment to the task
    if worker in task.assignees.all():
        task.assignees.remove(worker)
    else:
        task.assignees.add(worker)

    return redirect("task_manager:worker-detail", pk=worker.id)
