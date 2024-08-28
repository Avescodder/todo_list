from django import forms
from users.models import MyUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate



class RegistartionForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'confirm_password']


class LoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username_or_email, password=password)

        if user is None:
            try:
                from users.models import MyUser
                user_obj = MyUser.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
                print(user)
                if user is None:
                    raise forms.ValidationError("Invalid login credentials")
            except MyUser.DoesNotExist:
                raise forms.ValidationError("Invalid login credentials")

        return self.cleaned_data