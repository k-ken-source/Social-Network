from django.db import models
from users.models import Profile
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

class Task(models.Model):
	profile  = models.ForeignKey(Profile,on_delete = models.CASCADE)
	title = models.CharField(max_length = 200)
	description = models.CharField(max_length = 300)
	applicants = models.ManyToManyField(Profile, blank = True, related_name = 'Applicants')
	deadline  = models.DateField()
	date_posted = models.DateTimeField(default = timezone.now)

	def get_absolute_url(self):
		return reverse('task-home')