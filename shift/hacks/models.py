from django.db import models
from django.contrib.auth.models import AbstractUser

class Shifter(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/<username>/', null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

class Shift_post(models.Model):
    author = models.ForeignKey(Shifter, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField('Shift_comment', blank=True, related_name='post_comments')

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"

class Shift_comment(models.Model):
    author = models.ForeignKey(Shifter, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    child_comments = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"
