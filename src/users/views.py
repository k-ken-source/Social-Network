from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserRegister,UserUpdateForm,ProfileUpdateForm
from .models import Relationship, Profile
from blog.models import post
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def register(request):
	if request.method== 'POST':
		form = UserRegister(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to Log In')
			return redirect('login')
	else:
		form = UserRegister()
	
	return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
	if request.method== 'POST':
		u_form=UserUpdateForm(request.POST, instance=request.user)
		p_form=ProfileUpdateForm(request.POST, 
			request.FILES,
			instance=request.user.profile)
		

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()

			messages.success(request, f'Your account has been Updated!')
			return redirect('profile-edit')
	else:
		u_form=UserUpdateForm(instance=request.user)
		p_form=ProfileUpdateForm(instance=request.user.profile)
		

	context={
	'u_form':u_form,
	'p_form':p_form
	}
	return render(request,'users/profile.html',context)

class Profile_Detail_View(LoginRequiredMixin,DetailView):
	model = Profile
	template_name = 'users/profiledetail.html'
	context_object_name = 'object'


	def get_object(self):
		pk = self.kwargs.get('pk')
		user = User.objects.get(pk=pk)
		profile = Profile.objects.get(user = user)
		return profile

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pk = self.kwargs.get('pk')
		user = User.objects.get(pk=pk)
		profile  = Profile.objects.get(user = self.request.user)
		
		# LOGIC INVITE ALREDY FRIEND 
		rel_sender = Relationship.objects.filter(sender = profile)
		rel_rec = Relationship.objects.filter(reciever = profile)
	
		# Extract the other user i.e receiver of the realtion
		user_sender = []
		for obj in rel_sender:
			user_sender.append(obj.reciever.user)

		# Extract the other user i.e sender of the realtion
		user_rec = []
		for obj in rel_rec:
			user_sender.append(obj.sender.user)

		# Add to the context
		context['Profile'] = profile
		context['Sender'] = user_sender
		context['Rec'] = user_rec
		######################################

		Post_by_user = post.objects.get_all_posts_by_user(user)
		count = len(Post_by_user)

		context['count'] = count
		context['posts'] = Post_by_user

		return context
	

	'''	
	def get_queryset(self,pk):
		user = User.objects.get(pk = pk)
		pro = Profile.objects.get(user = user)
		return pro
	'''
@login_required
def Received_Invites(request):
	rel = Relationship.objects.invitations_recieved(request.user)
	qs = list(map(lambda x: x.sender,rel))
	is_empty= False
	if len(qs)==0:
		is_empty =True

	context ={"qs":qs, 'is_empty':is_empty}
	return render(request, 'users/My_invites.html',context)

@login_required
def accept_invitations(request):
	if request.method == 'POST':
		sender = Profile.objects.get(pk = request.POST.get('profile_pk'))
		rec = Profile.objects.get(user = request.user)
		relation = get_object_or_404(Relationship, sender =sender, reciever = rec)
		if relation.status == 'send':
			relation.status = 'accepted'
			relation.save()

		return redirect(request.META.get('HTTP_REFERER'))
	return redirect(request,'users/My_invites.html' )

@login_required
def reject_invitations(request):
	if request.method == 'POST':
		sender = Profile.objects.get(pk = request.POST.get('profile_pk'))
		rec = Profile.objects.get(user = request.user)
		relation = get_object_or_404(Relationship, sender =sender, reciever = rec)
		relation.delete()

		return redirect(request.META.get('HTTP_REFERER'))
	return redirect(request,'users/My_invites.html' )

@login_required
def withdraw (request):
	if request.method == 'POST':
		rec = Profile.objects.get(pk = request.POST.get('profile_pk'))
		sender = Profile.objects.get(user = request.user)
		relation = get_object_or_404(Relationship, sender =sender, reciever = rec)
		relation.delete()

		return redirect(request.META.get('HTTP_REFERER'))
	return redirect(request,'users/My_invites.html' )


@login_required
def Available_Profiles(request):
	qs = Profile.objects.get_all_profiles(request.user)
	context ={"qs":qs}

	return render(request, 'users/invites.html',context)


class ProfileListView(LoginRequiredMixin,ListView):
	model = Profile
	template_name = 'users/invites.html'
	context_object_name = 'qs'

	#Default Query method of the class view
	def get_queryset(self):
		query  = Profile.objects.get_all_profiles(self.request.user)
		return query
	
	# for passing additional values to content 
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user  = User.objects.get(username = self.request.user)
		profile = Profile.objects.get(user = user)

		rel_sender = Relationship.objects.filter(sender = profile)
		rel_rec = Relationship.objects.filter(reciever = profile)
	
		# Extract the other user i.e receiver of the realtion
		user_sender = []
		for obj in rel_sender:
			user_sender.append(obj.reciever.user)

		# Extract the other user i.e sender of the realtion
		user_rec = []
		for obj in rel_rec:
			user_sender.append(obj.sender.user)

		# Add to the context
		context['Profile'] = profile 
		context['Sender'] = user_sender
		context['Rec'] = user_rec
		return context

@login_required
def add_friends(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		reciever = Profile.objects.get(pk=pk)
		sender = Profile.objects.get(user = request.user)
		relation = Relationship.objects.create(reciever= reciever, sender = sender, status = 'send')

		return redirect(request.META.get('HTTP_REFERER'))
	return redirect('find')

@login_required
def remove_friends(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		reciever = Profile.objects.get(pk=pk)
		sender = Profile.objects.get(user = request.user)
		relation = Relationship.objects.get(
			(Q(sender = sender) & Q(reciever = reciever)) | (Q(sender= reciever) & Q(reciever = sender))
			)
		relation.delete()

		return redirect(request.META.get('HTTP_REFERER'))
	return redirect('find')

