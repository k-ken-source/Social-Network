from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from tinymce.models import HTMLField

class PostManager(models.Manager):
	def get_all_posts_by_user(self,user):
		p = post.objects.all().filter(author = user)
		return p

	def get_users_post_count(self,user):
		cnt = post.objects.all().filter(author=user).count()
		return cnt


class post(models.Model):
	title= models.CharField(max_length=100)
	thumbnail = models.ImageField( upload_to = 'Thumbnails',default = None)
	overview = models.TextField(default = "Overview")
	Liked = models.ManyToManyField(Profile,default=None)
	content = HTMLField()
	date_posted= models.DateTimeField(default=timezone.now)
	author= models.ForeignKey(User,on_delete=models.CASCADE)

	objects = PostManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})

	def liked_value(self):
		count = self.Liked.all().count()
		return count

class blog(models.Model):
	title = models.CharField(max_length=200)
	content = HTMLField()
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	#Liked = models.ManyToManyField(Profile,default = None)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog-detail', kwargs={'pk':self.pk})


class Comment(models.Model):
	user = models.ForeignKey(Profile,on_delete=models.CASCADE)
	post = models.ForeignKey(post, on_delete = models.CASCADE)
	date_posted = models.DateTimeField(default = timezone.now)
	content = models.CharField(max_length = 300)

	def __str__(self):
		return str(self.pk)

LIKE_CHOICES = {
	('like','like'),
	('unlike','unlike'),
}
class likes(models.Model):
	user  = models.ForeignKey(Profile, on_delete =models.CASCADE)
	post  = models.ForeignKey(post,on_delete= models.CASCADE)
	Status = models.CharField(max_length= 6, choices = LIKE_CHOICES)

	def __str__(self):
		return self.Status
