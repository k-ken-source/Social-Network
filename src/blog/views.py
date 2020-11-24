from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import post, likes, Comment
from users.models import Profile
from django.views.generic import (
ListView, 
DetailView, 
CreateView,
UpdateView,
DeleteView
)

from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


class PostListView(LoginRequiredMixin,ListView):
	model = post
	template_name='blog/home.html'
	context_object_name='posts'
	ordering=['-date_posted']
	paginate_by=5

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		profile = Profile.objects.get(user = self.request.user)
		context['user_profile'] = profile		
		return context

class UserPostListView(LoginRequiredMixin,ListView):
	model = post
	template_name='blog/user_posts.html'
	context_object_name='posts'
	ordering=['-date_posted']
	paginate_by=5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return post.objects.filter(author=user).order_by('-date_posted')


class DetailView(LoginRequiredMixin,DetailView):
	model = post
	form = CommentForm

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		post  = self.get_object()
		comments = Comment.objects.all().filter(post = post)
		context['comment'] = comments
		context['form'] = self.form
		return context


	def post(self, request, *args, **kwargs):
		form = CommentForm(request.POST)
		if form.is_valid():
			post = self.get_object()
			profile  = Profile.objects.get(user = request.user)
			form.instance.user = profile
			form.instance.post = post
			form.save()
			return redirect('post-detail', pk=post.pk)
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)  

class PostCreateView(LoginRequiredMixin, CreateView):
	model=post
	form_class = PostForm
#	fields=['title','content']
	
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = post
	#form_class = PostForm
	fields = ['title','overview','thumbnail','content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post=self.get_object()
		if self.request.user == post.author:
			return True 
		return False
		
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = post
	success_url = '/'
	def test_func(self):
		post=self.get_object()
		if self.request.user == post.author:
			return True
		return False


login_required
def likePost(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			pk = request.POST.get("post_pk")
			post_obj = post.objects.get(pk=pk)
			profile = Profile.objects.get(user = request.user)

			if profile in post_obj.Liked.all():
				post_obj.Liked.remove(profile)
			else:
				post_obj.Liked.add(profile)

			like, created  = likes.objects.get_or_create(user = profile, post = post_obj)
			# if created is true ie like was not there and has been created just now 
			if not created:
				if like.Status == 'like':
					like.Status = 'unlike'
					
				else:
					like.Status = 'like'
			else:
				like.Status = 'like'

				post_obj.save()
				like.save()

			return redirect(request.META.get('HTTP_REFERER'))
