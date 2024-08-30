
from typing import Any

import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import DetailView, ListView
from time import gmtime, strftime
from mainapp.forms import EditTaskForm, TaskForm
from mainapp.models import Status, Task


class TasksListView(ListView):
    model = Task
    template_name = "mainapp/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = super().get_queryset()
        tasks = tasks.filter(user=self.request.user)
        self.selected_statuses = self.request.POST.getlist("status", [])
        self.selected_statuses = [int(status_id) for status_id in self.selected_statuses]
        if self.selected_statuses:
            tasks = tasks.filter(status_id__in=self.selected_statuses)
        return tasks

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["date_time"] = strftime("%Y-%m-%d", gmtime())
        context["statuses"] = Status.objects.all()
        context["form_add"] = TaskForm()
        context["form_edit"] = EditTaskForm()
        context["selected_statuses"] = self.selected_statuses
        return context

    def post(self, request):
        if "edit_task_id" in request.POST:
            task_id = int(request.POST["edit_task_id"])
            task = Task.objects.get(id=task_id, user=request.user)
            form_edit = EditTaskForm(request.POST, request.FILES, instance=task)
            if form_edit.is_valid():
                form_edit.save()
                return HttpResponseRedirect(reverse("mainapp:index"))
        elif "add-task" in request.POST:
            form_add = TaskForm(request.POST, request.FILES)
            if form_add.is_valid():
                task = form_add.save(commit=False)
                task.user = request.user
                task.save()
            return HttpResponseRedirect(reverse("mainapp:index"))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


class TaskInfoView(DetailView):
    queryset = Task.objects.all()

    def get(self, request, pk):
        self.task = self.get_object()
        task_json = {
            "id": self.task.id,
            "title": self.task.title,
            "text": self.task.text,
            "img": self.task.img.url if self.task.img else "",
            "status": self.task.status.id,
            "category": self.task.category.id,
        }
        return JsonResponse(task_json)
