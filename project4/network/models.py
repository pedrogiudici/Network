from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userf')
    follows = models.ManyToManyField(User, related_name='followersf', blank=True)
    def __str__(self):
        return f'{self.user}'

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='postsp')
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likesp', blank=True)
    def serialize(self):
        return {
            'text': self.text,
            'likes': self.likes.count()
        }