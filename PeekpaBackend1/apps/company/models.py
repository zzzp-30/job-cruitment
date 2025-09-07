from django.db import models

# Create your models here.
class Company(models.Model):
    id = models.AutoField(primary_key=True)
    avatar = models.URLField()
    name = models.CharField(max_length=100)
    slogan = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    website = models.URLField()
    description = models.CharField(max_length=1000)