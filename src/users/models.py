from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models import Q


class ProfileManager(models.Manager):

	def get_all_profiles_to_invite(self,currUSer):
		# All Profiles without mine 
		profiles = Profile.objects.all().exclude(user ='currUSer')
		# Just my profile 
		myprofile =  Profile.objects.get(user= 'currUSer')
		# All the Realtionships where we are the sender or reciever
		queryset = Relationship.objects.filter(Q(sender = myprofile) | Q(reciever = myprofile))
		
		accepted = []
		for rel in queryset:
			if rel.status == 'accepted':
				accepted.append(rel.reciever)
				accepted.append(rel.sender)

		available = [profile for profile in profiles if profile not in accepted]

		return available

	def get_all_profiles(self, currUser):
		profiles = Profile.objects.all().exclude(user = currUser)
		return profiles




class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	Fname = models.CharField(max_length=100, blank=True)
	Lname = models.CharField(max_length=100, blank=True)
	
	image=models.ImageField(default='default.jpg',upload_to='Profile_pics')
	bio = models.CharField(max_length = 200, default='No Bio')
	Friends = models.ManyToManyField(User, blank =True, related_name = "friends")

	objects = ProfileManager()

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		#for image resizing 
		super().save(*args, **kwargs)

		img=Image.open(self.image.path)

		if img.height >300 or img.width >300:
			output=(300,300)
			img.thumbnail(output)
			img.save(self.image.path)

	def get_all_friends(self):
		return self.Friends.all()

	def get_all_friends_count(self):
		return self.Friends.all().count()
		

Status_Choice = (
	('send', 'send'),
	('accepted','accepted')
	)

class RelationshipManager(models.Manager):

	def invitations_recieved(self,reciever):
		r = Profile.objects.get(user=reciever)
		qs = Relationship.objects.filter(reciever =r, status='send')
		return qs


class Relationship(models.Model):
	sender = models.ForeignKey(Profile , on_delete=models.CASCADE, related_name ="sender")
	reciever = models.ForeignKey(Profile , on_delete=models.CASCADE, related_name ="reciever")
	status  = models.CharField(max_length = 8, choices = Status_Choice )

	objects = RelationshipManager()

	def __str__(self):
		return f"{self.sender}-{self.reciever}-{self.status}" 

