from django.db import models
from django.utils import timezone


# Create your models here.
# class Category(models.Model):
#     tag = models.CharField(max_length=100)

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    viewed = models.IntegerField(default=0, editable=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


