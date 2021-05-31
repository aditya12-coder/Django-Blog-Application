from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
# Create your models here.
class video(models.Model):
    sno=models.AutoField(primary_key=True)
    thumbnail = models.ImageField(upload_to='images/', null=True, blank=True) 

    videoLink=  models.CharField(max_length=255, null=True, blank=True)

    header=models.CharField(max_length=255)
    maker=models.CharField(max_length=14)
    pLanguage = models.CharField(max_length=50)
    link = models.SlugField(max_length=130, unique=True, blank=True)
    watcher= models.IntegerField(default=0)
    timeStamp=models.DateTimeField(blank=True)
    discription=models.TextField()
    code=models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.header)
        super(video, self).save(*args, **kwargs)


    def __str__(self):
        return self.header + " by " + self.maker


class Comment(models.Model):
    post = models.ForeignKey(video,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=False)
    body = models.TextField(blank=False, max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
