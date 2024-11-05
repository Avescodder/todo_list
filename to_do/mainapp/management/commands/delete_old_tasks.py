from django.core.management.base import BaseCommand
from django.utils import timezone
from mainapp.models import Task

class Command(BaseCommand):
    help = "Delete tasks older than one day"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        cutoff_time = now - timezone.timedelta(days=1)
        old_tasks = Task.objects.filter(date_time__lt=cutoff_time)
        count, _ = old_tasks.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} tasks older than one day'))