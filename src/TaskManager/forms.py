from django import forms
from .models import Task

class DateInput(forms.DateInput):
	input_type = 'date'

class TaskForm(forms.ModelForm):
	class Meta:
		model= Task
		fields = ['title','description', 'deadline']
		widgets = {'deadline' : DateInput()}
		