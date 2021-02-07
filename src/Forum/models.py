from django.db import models
from users.models import Profile
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

class thread(models.Model):
	author  = models.ForeignKey(Profile,on_delete = models.CASCADE)
	date_posted = models.DateTimeField(default = timezone.now)
	title  = models.CharField(max_length = 200)
	content = models.TextField()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('thread-detail', kwargs={'pk':self.pk})

class Replies(models.Model):
	author  = models.ForeignKey(Profile, on_delete = models.CASCADE)
	thread = models.ForeignKey(thread, on_delete = models.CASCADE)
	date_posted = models.DateTimeField(default = timezone.now)
	content  = models.TextField()

	def __str__(self):
		return self.author
