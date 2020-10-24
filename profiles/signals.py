from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from .models import Profile,Relationship


#Everytime a new user is created a profile of that user is automatically created
@receiver(post_save,sender= User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print('sender',sender)
    print('instance',instance)
    print(instance.__dict__)
    print(kwargs)
    if created:
        Profile.objects.create(user=instance,first_name=instance.first_name,last_name=instance.last_name,email=instance.email)


#When a user accepts a invitation add sender to receiver friend's list and vice versa 
@receiver(post_save, sender = Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()


#this signal will automatically remove friends from each other list when remove friends button is clicked
@receiver(pre_delete, sender = Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):    #instance is an obj of Relationship model
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)



    
    