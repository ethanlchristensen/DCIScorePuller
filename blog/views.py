from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Post, PostLike, PostComment

@login_required
def home(request):
    """
    View to render the home template
    """

    # get the tempalte name
    template = "blog/home.html"
    # get the title
    title = "Blog Home"
    # get the posts
    posts = Post.objects.all().order_by("-date")
    # get your likes
    likes = PostLike.objects.filter(user=request.user)
    # create the context
    context = {
        "title": title,
        "posts": posts,
        "likes": likes,
        "i_am": "blog"
    }
    # render the tempalte
    return render(request, template_name=template, context=context)

@login_required
def like_unlike_post(request, post_id):

    next = request.GET.get("next")

    post = Post.objects.get(id=post_id)
    like, like_created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not like_created:
        like.delete()
        post.user_likes.remove(request.user)
    else:
        post.user_likes.add(request.user)
    
    return redirect(next)
    
