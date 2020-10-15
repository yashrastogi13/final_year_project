from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile


# Create your models here.
class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', validators = [FileExtensionValidator(['png','jpg','jpeg'])], blank = True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return str(self.content[:50])

    def no_of_likes(self):
        return self.liked.all().count()

    def no_of_comments(self):
        #using set(reverse relationship) to access all comments linked to a 
        # post because there is not related name for post in comment class
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)    #newer post will be at the top and older post will be at bottom

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    #first value is for processing and second value is for admin
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  #related_name="user_likes"
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  #related_name="post_likes"
    value = models.CharField(choices = LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

    
