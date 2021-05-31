from django.contrib import admin
from video.models import video, Comment
# Register your models here.


@admin.register(video, Comment)

class videoAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinymc.js', )

