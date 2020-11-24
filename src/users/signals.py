from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver 
from .models import Profile, Relationship


@receiver(post_save,sender=User)
def create_profile(sender, instance , created ,**kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
		instance.profile.save()

@receiver(post_save, sender = Relationship)
def add_friend(sender,instance, created, **kwargs):
	sender_ = instance.sender
	reciever_ = instance.reciever

	if instance.status == "accepted":
		sender_.Friends.add(reciever_.user) #Friends List will contain User not profile ))#
		reciever_.Friends.add(sender_.user) 

		sender_.save()
		reciever_.save()

@receiver(pre_delete, sender = Relationship)
def remove_friends(sender, instance, **kwargs):
	Sender = instance.sender
	Rec = instance.reciever

	Sender.Friends.remove(Rec.user)
	Rec.Friends.remove(Sender.user)

	Sender.save()
	Rec.save()
	

