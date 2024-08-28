from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from mainapp.models import Status, Category, Task
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from mainapp.forms import TaskForm, EditTaskForm
from django.db.models import Q
from typing import Any
import logging


@login_required
def index(request):
    if request.method == 'POST':
        if 'edit_task_id' in request.POST:
            print('1')
            task_id = int(request.POST['edit_task_id'])
            task = Task.objects.get(id=task_id, user=request.user)
            form_edit = EditTaskForm(request.POST, request.FILES, instance=task)
            if form_edit.is_valid():
                form_edit.save()
                return HttpResponseRedirect(reverse('mainapp:index'))
        elif 'status' in request.POST:
            form_add = TaskForm()
            form_edit = EditTaskForm()
            selected_statuses = request.POST.getlist('status')
            if selected_statuses:
                selected_statuses = [int(status_id) for status_id in selected_statuses]
                tasks = Task.objects.filter(user=request.user, status_id__in=selected_statuses)
            else:
                tasks = Task.objects.filter(user=request.user)
            context = {
            'tasks': tasks,
            'statuses': Status.objects.all(),
            'form_add': form_add,
            'form_edit': form_edit, 
            'selected_statuses': selected_statuses,
            }
            return render(request, 'mainapp/index.html', context)
        else:
            form_add = TaskForm(request.POST, request.FILES)
            if form_add.is_valid():
                task = form_add.save(commit=False)
                task.user = request.user
                task.save()
            return HttpResponseRedirect(reverse('mainapp:index'))
            
    else:
        form_add = TaskForm()
        form_edit = EditTaskForm()
        tasks = Task.objects.filter(user=request.user)
        context = {
            'tasks': tasks,
            'statuses': Status.objects.all(),
            'form_add': form_add,
            'form_edit': form_edit, 
            'selected_statuses': [],
        }
        return render(request, 'mainapp/index.html', context)


class TasksListView(ListView):
    model = Task
    template_name = 'mainapp/index_2.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = super().get_queryset()
        tasks = tasks.filter(user=self.request.user)
        status_id = self.request.POST.getlist('status')
        if status_id:
            tasks = tasks.filter(status_id__in = status_id)
        return tasks
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()  
        context['form_add'] = TaskForm()
        context['form_edit'] = EditTaskForm()
        selected_statuses = self.request.POST.getlist('status', [])
        selected_statuses = [int(status_id) for status_id in selected_statuses]
        context['selected_statuses'] = selected_statuses
        return context
    
    def post(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)
    

    


    
class TaskInfoView(DetailView):
    queryset = Task.objects.all()

    def get(self, request, pk):
        self.task = self.get_object()
        task_json = {
            'id': self.task.id,
            'title': self.task.title,
            'text': self.task.text,
            'img': self.task.img.url if self.task.img else '',
            'status': self.task.status.id,
            'category': self.task.category.id,
        }
        return JsonResponse(task_json)