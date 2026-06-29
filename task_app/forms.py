from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User

from task_app.models import Task

class Createnewuser_form(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'date_completed']
