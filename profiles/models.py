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

    def get_no_of_post(self):
        #instead of using post_set.all().count() we are using related_name from post class
        return self.posts.all().count()

    def get_authors_post(self):
        return self.posts.all()

    def get_no_of_likes_given(self):
        #using related name from Like class in models 
        likes = self.like_set.all()
        total_likes = 0
        for item in likes:
            if item.value == 'Like':
                total_likes += 1
        return total_likes

    def get_no_of_likes_received(self):
        #using related name from Post model to get reverse relation for likes
        posts = self.posts.all()
        total_likes = 0
        for item in posts:
            #important
            #here related_name(likes) does not work becoz there is no reverse relationship
            #there is only forward relationship so we can directly use column name
            total_likes += item.liked.all().count()
        return total_likes

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

