from django.shortcuts import render,  redirect
from blog.models import Post, BlogComment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras
import requests

# Create your views here.
def blogHome(request):
    allPosts= Post.objects.all().order_by('-timeStamp')
    paginator = Paginator(allPosts, 6)
    page = request.GET.get('page')
    allPosts = paginator.get_page(page)
    context={'allPosts': allPosts}
    return render(request, "blog/blogHome.html", context)

def blogPost(request, slug):
    post=Post.objects.filter(slug=slug).first()
    allPosts= Post.objects.all()
    try:
        post.views= post.views +1
        post.save()
    except Exception as e:
        return render(request, 'home/error.html')

    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'allPosts': allPosts, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')


        if len(comment)<3:
            messages.error(request, "Your comment must contain more then 3 characters")
            return redirect(f"/blog/{post.slug}")



        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")




@login_required()
def commentHistory(request):

    if request.user.is_authenticated:   
        comments= BlogComment.objects.filter(user=request.user, parent=None)
        replies= BlogComment.objects.filter(user=request.user).exclude(parent=None)
        replyDict={}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno]=[reply]
            else:
                replyDict[reply.parent.sno].append(reply)

        context={ 'comments': comments, 'user': request.user, 'replyDict': replyDict}
        return render(request, "home/commentHistory.html", context)
    else:
        messages.error(request, 'You are not authenticated to view this page. Please login to see you comment history')
        return redirect('home')



