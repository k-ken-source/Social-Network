from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import TaskForm
from users.models import Profile 
from .models import Task 
from django.views.generic import (
ListView, 
DetailView, 
CreateView,
UpdateView,
DeleteView
)


class TaskListView(LoginRequiredMixin,ListView):
	model  = Task 
	ordering = ['-date_posted']
	context_object_name = 'posts'

class TaskCreateView(LoginRequiredMixin,CreateView):
	model  = Task 
	form_class = TaskForm

	def form_valid(self,form):
		p = Profile.objects.get(user = self.request.user)
		form.instance.profile = p
		return super().form_valid(form)

class TaskUpdateView(UserPassesTestMixin,UpdateView):
	model  = Task
	form_class = TaskForm

	def form_valid(self,form):
		p = Profile.objects.get(user = self.request.user)
		form.instance.profile = p
		return super().form_valid(form)

	def test_func(self):
		task = self.get_object()
		if self.request.user == task.profile.user:
			return True 
		return False

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Task 
	success_url = '/taskmanager'

	def test_func(self):
		task = self.get_object()
		if self.request.user == task.profile.user:
			return True 
		return False