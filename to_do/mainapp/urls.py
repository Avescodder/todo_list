from django.urls import path
from mainapp.views import TasksListView, TaskInfoView, CreateTeamView


app_name = "mainapp" 

urlpatterns = [
    path('', TasksListView.as_view(extra_context={'title':"extra_context"}), name='index'),
    path('tasks/<int:pk>/', TaskInfoView.as_view(), name='get_tasks_info'),
    path('add-team/', CreateTeamView.as_view(), name='add_team'),
]
