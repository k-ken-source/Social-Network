from django.shortcuts import render, redirect, reverse

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from users.models import Profile
from .models import thread, Replies
from .forms import RepliesForm

from django.views.generic import (
ListView, 
DetailView, 
CreateView,
UpdateView,
DeleteView
)

class ThreadListView(LoginRequiredMixin,ListView):
	model  = thread
	ordering = ['-date_posted']
	context_object_name = 'posts'

class ThreadDetailView(LoginRequiredMixin,DetailView):
	model = thread
	form = RepliesForm
	context_object_name = 'post'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		thread  = self.get_object()
		comments = Replies.objects.all().filter(thread = thread)
		context['comment'] = comments
		context['form'] = self.form
		return context


	def post(self, request, *args, **kwargs):
		form = RepliesForm(request.POST)
		if form.is_valid():
			thread = self.get_object()
			profile  = Profile.objects.get(user = self.request.user)
			form.instance.author = profile
			form.instance.thread = thread
			form.save()
			return redirect('thread-detail', pk=thread.pk)
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

class ThreadCreateView(LoginRequiredMixin,CreateView):
	model = thread
	fields = ['title', 'content']

	def get_success_url(self):
		return reverse('thread-detail', kwargs={'pk': self.object.pk})

	def form_valid(self,form):
		profile = Profile.objects.get(user  = self.request.user)
		form.instance.author = profile
		return super().form_valid(form)

class ThreadDeleteView(LoginRequiredMixin,DeleteView):
	model = thread
	success_url = '/forum'
	def test_func(self):
		thread = self.get_object()
		if self.request.user == thread.author.user:
			return True
		return False
class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
	model = thread
	fields = ['title', 'content']

	def form_valid(self,form):
		profile = Profile.objects.get(user  = self.request.user)
		form.instance.author  = profile
		return super().form_valid(form)

	def test_func(self):
		thread = self.get_object()
		if self.request.user == thread.author.user:
			return True 
		return False

