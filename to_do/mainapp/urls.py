from django.urls import path
from mainapp.views import TasksListView, TaskInfoView


app_name = "mainapp" 

urlpatterns = [
    path('', TasksListView.as_view(), name='index'),
    path('tasks/<int:pk>/', TaskInfoView.as_view(), name='get_tasks_info'),
]
