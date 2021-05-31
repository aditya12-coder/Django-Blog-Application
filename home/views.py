from django.shortcuts import render, HttpResponse, redirect
from .forms import SignUpForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, UserChangeForm, PasswordResetForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from validate_email import validate_email
from home.models import Contact, UserOTP
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Post
from django.core.mail import send_mail
import random
from video.models import video
import requests
import json

def error_404_view(request, exception):
    return render(request, 'home/error.html')

def home(request):
    return render(request, "home/home.html")


def teams(request):
    return render(request, "home/teams.html")


def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        ip= request.POST['info']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<5 or len(phone)<10 or len(content)<4 :
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name,ip_address=ip, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()

    if len(query)>78:
        messages.error(request, 'You query must not contain more then 78 character')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if len(query)<4:
        messages.error(request, 'You query must contain 4 character')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


def search2(request):
    result=request.GET['query2']

    if len(result)<4:
        messages.error(request, 'You query must contain 4 character')
        return redirect('/courses')

    if len(result)>78:
        allvideo= video.objects.none()

    if len(result)>78:
        messages.error(request, 'You query must not contain more then 78 character')
        return redirect('/courses')

    else:
        allvideoTitle=video.objects.filter(header__icontains=result)
        allvideoAuthor=video.objects.filter(maker__icontains=result)
        allvideoContent = video.objects.filter(discription__icontains=result)
        allvideo =  allvideoTitle.union(allvideoContent, allvideoAuthor)

    if (allvideo).count()==0:
        messages.warning(request, "No search results found. Please refine your query.")


    params={'allvideo': allvideo,  'result': result}
    return render(request, 'home/vsearch.html', params)


def signup(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')  # 213243 #None
        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)
            try:
                if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                    usr.is_active = True
                    usr.save()
                    messages.success(
                        request, f'Account is Created For {usr.username}')
                    return redirect('login')
                else:
                    messages.warning(request, f'You Entered a Wrong OTP')
                    return render(request, 'home/signup.html', {'otp': True, 'usr': usr})
            except Exception as e:
                e = messages.error(request, 'Only numbers are allowed while entering otp')
                return render(request, 'home/signup.html', {'otp': True, 'usr': usr})


        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('name').split(' ')

            usr = User.objects.get(username=username, email=email)
            usr.email = email
            usr.first_name = name[0]
            if len(name) > 1:
                usr.last_name = name[1]
            usr.is_active = False
            usr.save()
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)

            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to AIO - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )

            return render(request, 'home/signup.html', {'otp': True, 'usr': usr})

    else:
        form = SignUpForm()

    return render(request, 'home/signup.html', {'form': form})


def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET['usr']
        if User.objects.filter(username=get_usr).exists() and not User.objects.get(username=get_usr).is_active:
            usr = User.objects.get(username=get_usr)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to AIO - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )
            return HttpResponse("Resend")

    return HttpResponse("Can't Send ")



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        get_otp = request.POST.get('otp')  # 213243 #None

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)
            try:

                if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                    usr.is_active = True
                    usr.save()
                    login(request, usr)
                    return redirect('home')
                else:
                    messages.warning(request, f'You Entered a Wrong OTP')
                    return render(request, 'home/login.html', {'otp': True, 'usr': usr})
            except Exception as e:
                e = messages.error(request, 'Only numbers are allowed while entering otp')
                return render(request, 'home/login.html', {'otp': True, 'usr': usr})

        usrname = request.POST['username']
        passwd = request.POST['password']

        user = authenticate(request, username=usrname, password=passwd)  # None
        if user is not None:
            login(request, user)
            return redirect('home')
        elif not User.objects.filter(username=usrname).exists():
            messages.warning(
                request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')
        elif not User.objects.get(username=usrname).is_active:
            usr = User.objects.get(username=usrname)
            usr_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to AIO - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )
            return render(request, 'home/login.html', {'otp': True, 'usr': usr})
        else:
            messages.warning(
                request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login')

    form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/profile.html', {
        'form': form,

    })

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def about(request):
    return render(request, "home/about.html")

def myprofile(request):
    if request.user.is_authenticated:
        user.socialaccount_set.filter(provider='google')[0].extra_data['picture']
        return render(request, "home/profile.html")
    else:
        messages.error(request, "You are not authenticated to view this page.")
        return redirect('home')








class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")

        return email


