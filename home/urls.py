from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views
from home import views
from django.contrib.auth.views import LoginView

# from .views import UserEditView
urlpatterns = [
    path('', views.home, name="home"),

    path("password-reset/",
         PasswordResetView.as_view(
             template_name='home/password_reset.html'),
         name="password_reset"),
    path('contact', views.contact, name="contact"),

    path('teams', views.teams, name="teams"),

    path('search', views.search, name="search"),

    # path('profile', UserEditView.as_view(
    #     template_name='home/profile.html'), name='password_change'),

    path('profile', views.change_password, name='change_password'),

    path('query', views.search2, name="search2"),

    path('resendOTP', views.resend_otp),

    path('signup', views.signup, name="handleSignUp"),

    path('login', views.login_view, name="login"),


    path('logout', views.handelLogout, name="handleLogout"),

    path("password-reset/done/",
         PasswordResetDoneView.as_view(
             template_name='home/password_reset_done.html'),
         name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(
             template_name='home/password_reset_confirm.html'),
         name="password_reset_confirm"),

    path("password-reset-complete/",
         PasswordResetCompleteView.as_view(
             template_name='home/password_reset_complete.html'),
         name="password_reset_complete"),

]
