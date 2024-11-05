from django.db import models
from users.models import MyUser

class Status(models.Model):
    name = models.CharField(max_length=100)
    status_color = models.CharField(max_length=7)
    def __str__(self):
        return f"{self.id}. {self.name}"
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.id}. {self.name}"
    

class Team(models.Model):
    title = models.TextField(max_length=25)
    users = models.ManyToManyField(MyUser, related_name="teams")
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('In progress', 'In Progress'),
        ('done ', 'Completed'),
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=1)
    title = models.TextField(default='-', max_length=255)
    text = models.TextField(max_length=500)
    img = models.ImageField(upload_to='task_images/', null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.title


