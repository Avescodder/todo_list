from django import forms
from mainapp.models import Category, Task, Status


class RegistartionForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ['username', 'email', 'password', 'confirm_password']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'text', 'img', 'status', 'category']

class EditTaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'id':'id_title_edit', 'class':'textfields', 'rows':'3', 'cols':'30' }))
    text = forms.CharField(widget=forms.Textarea(attrs={'id':'id_text_edit', 'class':'textfields', 'rows':'3', 'cols':'30' }))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'id':'id_category_edit'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), widget=forms.Select(attrs={'id':'id_status_edit'}))
    img = forms.ImageField(widget=forms.FileInput(attrs={'id':'id_img_edit', 'class':'a'}), required=False)
    class Meta:
        model = Task
        fields = ['title', 'text', 'img', 'status', 'category']