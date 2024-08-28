from django.test import TestCase
from mainapp.models import Category, Status, Task
from users.models import MyUser
class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Test Category')
    
    def test_category_name_label(self):
        category=Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_category_name_max_length(self):
        category=Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

class TaskModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        Category.objects.create(name='Today')
        Status.objects.create(name='Test Status', status_color='#FF0000')
        MyUser.objects.create(username='testuser')

        Task.objects.create(title='Test Task', text='Test Task',
                               status=Status.objects.get(id=1),
                                 category=Category.objects.get(id=1),
                                  date_time='2022-01-01 00:00:00',
                                  user=MyUser.objects.get(id=1))
    def test_task_title_label(self):
        task=Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')
    
    def test_task_title_max_length(self):
        task=Task.objects.get(id=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)
    
    def test_task_text_label(self):
        task=Task.objects.get(id=1)
        field_label = task._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_task_text_max_length(self):
        task=Task.objects.get(id=1)
        max_length = task._meta.get_field('text').max_length
        self.assertEqual(max_length, 500)
    

    def test_task_date_time(self):
        task=Task.objects.get(id=1)
        field_label = task._meta.get_field('date_time').verbose_name
        self.assertEqual(field_label, 'date time')

    def test_task_status(self):
        task=Task.objects.get(id=1)
        field_label = task._meta.get_field('status').verbose_name
        self.assertEqual(field_label,'status')

    def test_task_category(self):
        task=Task.objects.get(id=1)
        field_label = task._meta.get_field('category').verbose_name
        self.assertEqual(field_label,'category')

    
class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='Test Status', status_color='#FF0000')

    def test_status_name_label(self):
        status=Status.objects.get(id=1)
        field_label = status._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_status_name_max_length(self):
        status=Status.objects.get(id=1)
        max_length = status._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_status_status_color_label(self):
        status=Status.objects.get(id=1)
        field_label = status._meta.get_field('status_color').verbose_name
        self.assertEqual(field_label,'status color')
    
    def test_status_status_color_max_length(self):
        status=Status.objects.get(id=1)
        max_length = status._meta.get_field('status_color').max_length
        self.assertEqual(max_length, 7)



