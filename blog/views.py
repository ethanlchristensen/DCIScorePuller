from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import CommentForm, CreatePostForm, UpdatePostForm, UpdateCommentForm
from .models import Post, PostComment, PostLike


@login_required
def home(request):
    """
    View to render the home template
    """

    # get the pagination page
    page = request.GET.get("page", 1)
    # get the tempalte name
    template = "blog/home.html"
    # get the title
    title = "Blog Home"
    # get the posts
    all_posts = Post.objects.all().order_by("-created_date")
    # paginate
    paginator = Paginator(all_posts, 5)
    # get that page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # get your likes
    likes = PostLike.objects.filter(user=request.user)
    # create the context
    context = {"title": title, "posts": posts, "likes": likes, "i_am": "blog"}
    # render the tempalte
    return render(request, template_name=template, context=context)

@login_required
def create_post(request):
    """
    View to render the create post template
    """

    # get the template
    template = "blog/create_post.html"
    # get the title
    title = "Create Blog Post"
    # create the context
    context = {"title": title, "i_am": "blog"}

    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(
                author=request.user,
                title=form.cleaned_data.get("title"),
                content=form.cleaned_data.get("content"),
            )

            return redirect("blog-home")
    else:
        form = CreatePostForm()

        context["form"] = form

    # render the template
    return render(request, template_name=template, context=context)

@login_required
def delete_post(request, post_id):
    next = request.GET.get("next")

    # did we come from a view-post url?
    prev_post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)

    if post:
        post.delete()
        messages.success(request, "Post was successfully deleted")
    else:
        messages.warning(request, "Post does not exist, or was already deleted")

    if prev_post_id:
        return redirect(reverse(next, args=(prev_post_id,)))
    else:
        return redirect(next)

@login_required
def update_post(request, post_id):
    """
    View to render the update post template
    """

    # get the template
    template = "blog/update_post.html"
    # get the title
    title = "Update Blog Post"
    # create the context
    context = {"title": title, "i_am": "blog"}

    next = request.GET.get("next")

    # did we come from a view-post url?
    prev_post_id = request.GET.get("post_id")

    if request.method == "POST":
        form = UpdatePostForm(request.POST)
        if form.is_valid():
            try:
                post = Post.objects.filter(id=post_id)
                post.update(title=form.cleaned_data["title"], content=form.cleaned_data["content"])
                # to update last_updated_date . . .
                post.first().save()
                messages.info(request, "Post was updated successfully")
            except Exception as exception:
                messages.warning(request, "A problem occured and the Post could not be updated")
    else:
        post = Post.objects.get(id=post_id)
        if request.user == post.author:
            form = UpdatePostForm(instance=post)
            context["post_id"] = post_id
            context["form"] = form
            return render(request, template_name=template, context=context)

    if prev_post_id:
        return redirect(reverse(next, args=(prev_post_id,)))
    else:
        return redirect(next)

@login_required
def like_unlike_post(request, post_id):
    next = request.GET.get("next")

    # did we come from a view-post url?
    prev_post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)
    like, like_created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not like_created:
        like.delete()
        post.user_likes.remove(request.user)
    else:
        post.user_likes.add(request.user)

    if prev_post_id:
        return redirect(reverse(next, args=(prev_post_id,)))
    else:
        return redirect(next)

@login_required
def view_post(request, post_id):
    """
    View to render out the view post template
    """

    # get the template
    template = "blog/view_post.html"
    # get the title
    title = "View Blog Post"
    # get the post
    post = Post.objects.filter(id=post_id).first()
    # comment form
    comment_form = CommentForm()
    # get the existing comments
    comment_objects = PostComment.objects.filter(post=post).order_by("-last_updated_date")
    # create the context
    context = {
        "title": title,
        "i_am": "blog",
        "post": post,
        "comment_form": comment_form,
        "comments": comment_objects,
    }

    # render the template
    return render(request, template_name=template, context=context)

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        comment = CommentForm(request.POST)

        if comment.is_valid():
            post = Post.objects.filter(id=post_id).first()

            new_comment = PostComment(
                user=request.user, post=post, comment=comment.cleaned_data.get("comment")
            )

            new_comment.save()

        return redirect(reverse("view-post", args=(post_id,)))

@login_required
def get_comment_data_modal(request, post_id, comment_id):
    comment = PostComment.objects.filter(id=comment_id).first()
    update_comment_form = UpdateCommentForm(instance=comment)

    # get the template
    template = "blog/view_post.html"
    # get the title
    title = "View Blog Post"
    # get the post
    post = Post.objects.filter(id=post_id).first()
    # comment form
    comment_form = CommentForm()
    # get the existing comments
    comment_objects = PostComment.objects.filter(post=post).order_by("-last_updated_date")
    # create the context
    context = {
        "title": title,
        "i_am": "blog",
        "post": post,
        "comment_form": comment_form,
        "comments": comment_objects,
        "update_comment_form": update_comment_form,
        "update_comment_id": comment_id
    }

    # render the template
    return render(request, template_name=template, context=context)

@login_required
def update_comment(request, post_id, comment_id):
    if request.method == "POST":
        form = UpdateCommentForm(request.POST)

        if form.is_valid():
            comment = PostComment.objects.filter(id=comment_id)
            comment.update(
                comment = form.cleaned_data.get("comment")
            )
            comment.first().save()

            return redirect(reverse("view-post", args=(post_id,)))

@login_required
def delete_comment(request, post_id, comment_id):
    comment = PostComment.objects.filter(id=comment_id)

    if not comment.first().user == request.user:
        messages.error(request, "This is not your comment to delete")
        return redirect(reverse("view-post", args=(post_id,)))

    comment.delete()
    return redirect(reverse("view-post", args=(post_id,)))

