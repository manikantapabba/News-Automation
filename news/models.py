from django.db import models
from account.models import MyUser

# Create your models here.
class News_Update(models.Model):
    newspaper = models.CharField(primary_key=True,max_length=20)
    sports = models.CharField(max_length=1000,default="no news")
    technology = models.CharField(max_length=1000,default="no news")
    business = models.CharField(max_length=1000,default="no news")
    entertainment = models.CharField(max_length=1000,default="no news")


    def __str__(self):
        return self.newspaper

#model for user preferences
class Prefer(models.Model):
    email = models.EmailField(max_length=60,unique=True)
    sports = models.CharField(max_length=20,default="none")
    technology = models.CharField(max_length=20,default="none")
    business = models.CharField(max_length=20,default="none")
    entertainment = models.CharField(max_length=20,default="none")
    msg_type = models.CharField(max_length=20,default="mail")
    sent = models.CharField(max_length=20,default="nsent")
    def __str__(self):
        return self.email
