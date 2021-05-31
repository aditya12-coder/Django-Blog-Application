from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
import random, string


def random_id_field():
  rnd_id = ''.join(random.choices(string.ascii_letters + string.digits, k=11))
  return rnd_id


class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    title=models.CharField(max_length=255)
    author=models.CharField(max_length=14)
    slug=models.SlugField(max_length=130, unique=True, blank=True, default=random_id_field)
    views= models.IntegerField(default=0)
    timeStamp=models.DateTimeField(blank=True)
    content=models.TextField()


    def __str__(self):
        return self.title + " by " + self.author

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Post, self).save(*args, **kwargs)
        

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
    
