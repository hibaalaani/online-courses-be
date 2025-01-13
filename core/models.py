# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
class Topic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    branch = models.CharField(max_length=50, choices=[
        ('learn', 'Learn'),
        ('build', 'Build'),
    ])

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    tools = models.TextField()

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_date = models.DateField()
    session_time = models.TimeField()
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ])
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.session_date} {self.session_time}"




class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
    

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    