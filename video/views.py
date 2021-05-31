from django.shortcuts import render, redirect, HttpResponse
from video.models import video 
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
def videos(request):
	allvideo = video.objects.all()
	context={'allvideo': allvideo}
	return render(request, 'video/videoHome.html', context)



def videoPost(request, slug):
	vdi=video.objects.filter(link=slug).first()

	try:
		vdi.watcher = vdi.watcher +1
		vdi.save()
	except Exception as e:
		return render(request, 'home/error.html')
	allvideo=video.objects.all()	
	post = get_object_or_404(video, link=slug)
	comments = post.comments.filter(active=False)
	new_comment = None
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
			messages.success(request, 'Your comment has been posted successfully')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			messages.error(request, 'Invalid Comment')
			# return HttpResponseRedirect(request.META.get('HTTP_REFERER'))	
			return redirect(f"/courses/{post.link}")	
	else:
		comment_form = CommentForm()
		return render(request, 'video/videoPost.html', {	'video':vdi, 	'allvideo': allvideo, 
				'post': post,
                'comments': comments,
                'new_comment': new_comment,
                 'comment_form': comment_form
		})





