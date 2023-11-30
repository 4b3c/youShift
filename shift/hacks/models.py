from django.db import models
from django.contrib.auth.models import User

class Shift_post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField('Shift_comment', blank=True, related_name='post_comments')

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"

class Shift_comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    child_comments = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"
