from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    ip_address = models.CharField(blank=True,max_length=255)
    name = models.CharField(max_length=255)
    ip_data = models.TextField(blank=True)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Message from " + self.name + ' - ' + self.email




class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now=True)
    otp = models.SmallIntegerField()




