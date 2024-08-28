from django.contrib import admin
from django.urls import path, include
from mainapp.views import index, TasksListView,TaskInfoView
from django.views.decorators.cache import cache_page


app_name = "mainapp" 

urlpatterns = [
    path('', index, name='index'),
    path('tasks/<int:pk>/', TaskInfoView.as_view(), name='get_tasks_info'),
    path('main', TasksListView.as_view(), name='index_2')
]
