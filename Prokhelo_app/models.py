from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/user_images/')
    private_token = models.CharField(max_length=100)

class Admin(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    private_token = models.CharField(max_length=100)