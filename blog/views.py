import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils.text import slugify
from django.contrib import messages
from django.core.paginator import Paginator

from .models import BlogPost, Category, Tag, Comment, Save
from .forms import BlogPostForm, CommentForm

from .helpers import create_page_range


# Create your views here.
def home(request):
    return render(request, "blog/home.html")


def explore(request):
    query = request.GET.get("query", "")

    # Search (Filter) posts
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query)  # Look in title
            | Q(caption__icontains=query)  # Look in caption
            # | Q(content__icontains=query)  # Look in content
        )
    else:
        posts = BlogPost.objects.all()

    # Get all categories
    categories = Category.objects.all()

    # Paginations
    page_number = request.GET.get("page")
    paginator = Paginator(posts, 20)  # 20 posts per page
    page_obj = paginator.get_page(page_number)

    # Create the page range
    page_range = create_page_range(list(paginator.page_range), page_obj.number, 5)

    return render(
        request,
        "blog/explore.html",
        {
            "page_obj": page_obj,
            "page_range": page_range,
            "categories": categories,
            "query": query,
            # "all_posts_count": BlogPost.objects.count(),
            # "category_slug": category,
        },
    )


# Not in USE (kept as backup)
def category(request, slug):
    posts = BlogPost.objects.filter(category__slug=slug.lower())

    # Get all categories
    categories = Category.objects.all()

    # Paginations
    page_number = request.GET.get("page")
    paginator = Paginator(posts, 20)  # 20 posts per page
    page_obj = paginator.get_page(page_number)

    # Create the page range
    page_range = create_page_range(list(paginator.page_range), page_obj.number, 5)

    return render(
        request,
        "blog/explore.html",
        {
            "page_obj": page_obj,
            "page_range": page_range,
            "categories": categories,
            "category_slug": slug,
            # "all_posts_count": BlogPost.objects.count(),
        },
    )


def search(request):
    query = request.GET.get("query", "")
    sort_by = request.GET.get("sort", "")

    sort_options = {
        "newest": "-created_at",
        "oldest": "created_at",
        "most-liked": "-like_count",
    }

    posts = (
        BlogPost.objects.filter(
            Q(title__icontains=query)  # Look in title
            | Q(caption__icontains=query)  # Look in caption
            | Q(content__icontains=query)
        )
        .annotate(like_count=Count("likes"))
        .order_by(sort_options.get(sort_by, "-created_at"))
    )

    return render(
        request,
        "blog/search.html",
        {
            "posts": posts,
            "query": query,
            "sort_by": sort_by,
        },
    )


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    saved = liked = already_following = user_posts = None

    # User Not Yet Deleted?
    if post.author:
        # User's 4 Other Posts
        user_posts = list(post.author.posts.all())

        # Check if already following
        if request.user.is_authenticated:
            already_following = post.author.followers.filter(
                follower_id=request.user.id
            )

    # Already Saved, Liked, Followed?
    if request.user.is_authenticated:
        saved = post.saves.filter(user=request.user)
        liked = post.likes.filter(user=request.user)

    form = CommentForm()
    return render(
        request,
        "blog/blog_detail.html",
        {
            "post": post,
            "user_posts": user_posts,
            "comment_form": form,
            "post_saved": saved[0] if saved else None,
            "post_liked": liked[0] if liked else None,
            "already_following": already_following,
        },
    )


@login_required(login_url="/accounts/login/")
def create_post(request):
    if request.method == "POST":
        # Get and Clean Tags
        tags = [slugify(tag) for tag in request.POST.getlist("all_tags")]
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Create Tags (non-existent ones only)
            for tag_name in tags:
                if tag_name:
                    Tag.objects.get_or_create(name=tag_name)

            blog = form.save()
            blog.author = request.user
            blog.tags.add(*Tag.objects.filter(name__in=tags))
            blog.save()

            return redirect("blog_detail", slug=blog.slug)
    else:
        form = BlogPostForm()

    return render(
        request,
        "blog/create_post.html",
        {
            "form": form,
            "all_tags": Tag.objects.all(),
        },
    )


@login_required(login_url="/accounts/login/")
def edit_post(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug, author=request.user)

    if request.method == "POST":
        # Get and Clean Tags
        tags = [slugify(tag) for tag in request.POST.getlist("all_tags")]
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            # Remove (from blogpost) tags that are not in submitted tags
            for tag in blog.tags.all():
                if tag.name not in tags:
                    blog.tags.remove(tag)

            # Create Tags (non-existent ones only)
            for tag_name in tags:
                if tag_name:
                    Tag.objects.get_or_create(name=tag_name)

            blog = form.save(commit=False)
            blog.tags.add(*Tag.objects.filter(name__in=tags))
            blog.save()

            return redirect("blog_detail", slug=blog.slug)
    else:
        # GET request
        form = BlogPostForm(instance=blog)

    return render(
        request,
        "blog/edit_post.html",
        {
            "form": form,
            "form_tags": blog.tags.all(),
            "all_tags": Tag.objects.all(),
        },
    )


@login_required(login_url="/accounts/login/")
def delete_post(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug, author=request.user)

    if request.method == "POST":
        # TODO: delete the cover image also...
        blog.delete()
        return redirect("explore")

    return redirect("blog_detail", slug=slug)


# Like/Unlike post (Unlikes already liked post)
@login_required(login_url="/accounts/login/")
def like_post(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)

    if request.method == "POST":
        # Check if user already liked it
        like, created = blog.likes.get_or_create(user_id=request.user.id)

        # Like, if not!
        if created:
            like.post = blog
            like.save()
        else:
            # Unlike it.
            like.delete()

    return redirect("blog_detail", slug=slug)


# Comment on a post
@login_required(login_url="/accounts/login/")
def comment_on_post(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)

    if request.method == "POST":
        comment = Comment.objects.create(
            user=request.user, post=blog, content=request.POST.get("content")
        )
        comment.save()

    return redirect("blog_detail", slug=slug)


# Save posts
@login_required(login_url="/accounts/login/")
def save_post(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)

    if request.method == "POST":
        # Check if user already Saved it
        save, created = blog.saves.get_or_create(user_id=request.user.id)

        # save, if not!
        if created:
            save.post = blog
            save.save()
        else:
            # Unsave it.
            save.delete()

    return redirect("blog_detail", slug=slug)


# Delete Saved post
@login_required(login_url="/accounts/login/")
def delete_saved(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)

    if request.method == "POST":
        # Check if user even Saved it
        # save = blog.saves.get(user_id=request.user.id)
        save = get_object_or_404(blog.saves, user_id=request.user.id)

        # Unsave it.
        save.delete()

    return redirect("users:user_profile", username=request.user.username)
