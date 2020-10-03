from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .utils import get_random_code
from django.template.defaultfilters import slugify
# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length = 200, blank = True)
    last_name = models.CharField(max_length = 200, blank = True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    bio = models.TextField(default = "no bio", max_length=300, blank = True)
    email = models.EmailField(max_length = 200,blank = True)
    country = models.CharField(max_length = 100,blank = True)
    avatar = models.ImageField(default = "avatar.png", upload_to = 'avatars/')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name='friends')
    slug = models.SlugField(unique = True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created =  models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"


    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name)+" "+str(self.last_name))
            #checking if the slug is already present
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args,**kwargs)


    #return friends of the user logged in
    def get_friends(self):
        return self.friends.all()

    #return count of friends of user logged in
    def get_friends_no(self):
        return self.friends.all().count()






STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted'),
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(choices = STATUS_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created =  models.DateTimeField(auto_now_add=True)

    def __Str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"



