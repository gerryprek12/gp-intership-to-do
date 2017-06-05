import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from app.models import List, Task, PRIORITY_OPTIONS


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class ListForm(forms.Form):
    name = forms.CharField(max_length=60, required=True, help_text='Enter the name of the list.')
    priority = forms.ChoiceField(choices=PRIORITY_OPTIONS,required=True)
    assigned_to = forms.ModelChoiceField(User.objects.all(), required=False, label='Assign To')
    due_date = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y"), required=True, label='Due Date')


class TaskForm(forms.Form):
    title = forms.CharField(max_length=140, required=True, help_text='Enter the name of task.')
    priority = forms.ChoiceField(choices=PRIORITY_OPTIONS,required=True)
    assigned_to = forms.ModelChoiceField(User.objects.all(), required=False, label='Assign To')
    due_date = forms.DateField(required=True, label='Due Date')
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False, label='Note')

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False, label='Comment')