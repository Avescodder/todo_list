from django.test import TestCase
from mainapp.forms import RegistartionForm, TaskForm, EditTaskForm
from mainapp.models import Status, Category, Task
from users.models import MyUser


class TaskFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.status = Status.objects.create(name='Test Status', status_color='#FF0000')
        cls.category = Category.objects.create(name='Test Category')

    def test_task_form_valid(self):
        form_data = {
            'title': 'Test Task',
            'text': 'This is a test task.',
            'img': None,
            'status': 1,
            'category': 1,
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_task_form_invalid_title(self):
        form_data = {
            'title': '',
            'text': 'This is a test task.',
            'img': None,
            'status': 1,
            'category': 1,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_task_form_invalid_text(self):
        form_data = {
            'title': 'Test Task',
            'text': '',
            'img': None,
            'status': 1,
            'category': 1,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_form_invalid_status(self):
        form_data = {
            'title': 'Test Task',
            'text': 'This is a test task.',
            'img': None,
            'status': 0,
            'category': 1,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

class RegistrationFormTest(TestCase):

    def test_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'test123',
            'confirm_password': 'test123',
        }
        form = RegistartionForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_invalid_username(self):
        form_data = {
            'username': '',
            'email': 'testuser@example.com',
            'password': 'test123',
            'confirm_password': 'test123',
        }
        form = RegistartionForm(data=form_data)
        self.assertFalse(form.is_valid())

class EditTaskFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.status = Status.objects.create(name='Test Status', status_color='#FF0000')
        cls.category = Category.objects.create(name='Test Category')
        cls.task = Task.objects.create(title='Test Task', text='This is a test task.', status=cls.status, category=cls.category)
        cls.user = MyUser.objects.create(username='testuser')

    def test_edit_task_form_valid(self):
        form_data = {
            'title': 'Updated Test Task',
            'text': 'This is an updated test task.',
            'status': 1,
            'category': 1,
        }
        form = EditTaskForm(instance=self.task, data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_task_form_invalid_title(self):
        form_data = {
            'title': '',
            'text': 'This is an updated test task.',
            'status': 1,
            'category': 1,
        }
        form = EditTaskForm(instance=self.task, data=form_data)
        self.assertFalse(form.is_valid())