from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.videos, name="videos"),
    path('<str:slug>', views.videoPost, name="videoPost"),
]