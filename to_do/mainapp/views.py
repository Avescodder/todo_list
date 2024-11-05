from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import DetailView, ListView
from mainapp.forms import EditTaskForm, TaskForm, TeamForm
from mainapp.models import Status, Task
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import TitleStatusMixin

from django.views import View
from django.shortcuts import render, redirect
from .forms import TeamForm

class CreateTeamView(LoginRequiredMixin, View):
    def get(self, request):
        team_form = TeamForm()
        return render(request, 'mainapp/team_create.html', {'team_form': team_form})

    def post(self, request):
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            team = team_form.save()
            team.users.add(request.user) 
            return redirect('mainapp:index')
        return render(request, 'mainapp/team_create.html', {'team_form': team_form})
    

class TasksListView(LoginRequiredMixin, TitleStatusMixin, ListView):
    model = Task
    template_name = "mainapp/index.html"
    context_object_name = "tasks"
    title = 'mixin'
    paginate_by = 2

    def get_queryset(self):
        tasks = super().get_queryset()
        tasks = tasks.filter(user=self.request.user)
        
        selected_team = self.request.session.get("team_selected") if self.request.session.get("team_selected") != 0 else None
        
    
        tasks = tasks.filter(team_id = selected_team)
        
        self.selected_statuses = self.request.POST.getlist("status", [])
        self.selected_statuses = [int(status_id) for status_id in self.selected_statuses]
        
        if self.selected_statuses:
            tasks = tasks.filter(status_id__in=self.selected_statuses)
        
        return tasks

    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["team_selected"] = self.request.session.get('team_selected', 0)
        context["team_form"] = TeamForm()
        context["form_add"] = TaskForm()
        context["form_edit"] = EditTaskForm()
        context["selected_statuses"] = self.selected_statuses
        return context

    def post(self, request):
        print(self.request.session.get('test'))
        print(request.POST.get('team'))
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
                task.team_id = self.request.session.get("team_selected") if self.request.session.get("team_selected") != 0 else None
                task.save()
            return HttpResponseRedirect(reverse("mainapp:index"))
        elif "team" in request.POST:
            self.request.session["team_selected"] = int(request.POST.get('team'))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        self.request.session['test'] = 'a'
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
    
    
    