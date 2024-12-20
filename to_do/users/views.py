from django.shortcuts import render, redirect
from users.forms import RegistartionForm, LoginForm
from django.contrib.auth import login
from users.models import MyUser, VerParam
from mainapp.models import Task
from django.views.generic import View, TemplateView
from django.urls import reverse
from django.contrib.auth import logout
import uuid
import datetime

def register(request):
    if request.method == 'POST':
        form = RegistartionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            
            # Check if the two passwords match
            if password == confirm_password:
                # Instead of manually hashing the password, use MyUser's manager to create the user
                # This assumes MyUser's manager has a method like create_user similar to Django's User model
                user = MyUser.objects.create_user(username=username, email=email, password=password)
                verif = VerParam.objects.create(user = user, key = uuid.uuid4(), experation = datetime.datetime.now() + datetime.timedelta(minutes=5))
                verif.save()
                return redirect(reverse('mainapp:index'))
            else:
                # If passwords do not match, add an error to the form
                form.add_error('confirm_password', 'Password and confirm password do not match')
    else:
        form = RegistartionForm()
    
    return render(request, 'users/registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            from django.contrib.auth import authenticate
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(username=username_or_email, password=password)
            if not user:
                # Try to authenticate by email if the username fails
                from users.models import MyUser
                try:
                    user_obj = MyUser.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except MyUser.DoesNotExist:
                    pass
            else:
                login(request, user)
                return redirect(reverse('mainapp:index'))  # Redirect to a success page.
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

class UserLogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect(reverse('mainapp:index'))



class UserProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request):
        username = request.user.username
        return render(request, self.template_name, {'username': username})

    def post(self, request):
        task_count = Task.objects.filter(status_id=1, user=request.user).count()
        return render(request, self.template_name, {
            'username': request.user.username,
            'task_count': task_count
        })
    
class UserVerifyEmailView(TemplateView):
    template_name = 'users/verify_email.html'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        try:
            key = kwargs['key']
            print(key)
            verif = VerParam.objects.get(key=key)
            print(verif.experation.replace(tzinfo=None))
            print(datetime.datetime.now())
            if verif.experation.replace(tzinfo=None) > datetime.datetime.now():
                user = verif.user
                user.is_verified = True
                user.save()
                verif.delete()
                return render(request, self.template_name, {'success': True})
            else:
                return render(request, self.template_name, {'success': False, 'expired': True})
        except VerParam.DoesNotExist:
            return render(request, self.template_name, {'success': False, 'expired': False})
    
    
    


