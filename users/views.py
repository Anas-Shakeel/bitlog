from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from blog.helpers import create_page_range

from .models import Profile, Subscription
from .forms import ProfileForm
from accounts.models import User


# Create your views here.
def profile_view(request, username):
    # Get the User
    user = get_object_or_404(User, username=username)

    # Get the Profile of `user`
    profile = get_object_or_404(Profile, user=user)

    # Get Subscriptions
    followers = profile.user.followers.all()
    followings = profile.user.followings.all()
    already_following = user.followers.filter(follower_id=request.user.id)

    # Paginations
    user_posts = profile.user.posts.all()
    page_number = request.GET.get("page")
    paginator = Paginator(user_posts, 20)  # 20 posts per page
    page_obj = paginator.get_page(page_number)

    # Create the page range
    page_range = create_page_range(list(paginator.page_range), page_obj.number, 5)

    return render(
        request,
        "users/profile.html",
        {
            "profile": profile,
            "page_obj": page_obj,
            "page_range": page_range,
            "followers": followers,
            "followings": followings,
            "already_following": already_following,
            "show_author": "false",
        },
    )


@login_required(login_url="/accounts/login/")
def profile_saved_view(request):
    # Get the saved of user
    saved_posts = request.user.save_set.all()

    return render(
        request,
        "snippets/profile_saved_posts.html",
        {
            "page_obj": saved_posts,
        },
    )


@login_required(login_url="/accounts/login/")
def profile_edit(request, username):
    # Get the User (Authenticated User)
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("users:user_profile", username=username)
    else:
        # GET request
        form = ProfileForm(instance=profile)

    return render(
        request,
        "users/profile_edit.html",
        {
            "profile": profile,
            "form": form,
        },
    )


@login_required(login_url="/accounts/login/")
def profile_follow(request, username):
    user = get_object_or_404(User, username=username)

    if request.user.is_authenticated and (request.user != user):
        # Check if already followed
        already_following = user.followers.filter(follower_id=request.user.id)
        if already_following:
            return redirect("users:user_profile", username=user.username)

        # Follow user
        followed = Subscription.objects.create(follower=request.user, following=user)
        followed.save()

    return redirect(request.META.get("HTTP_REFERER"))

    # Return back to user's profile (LEGACY)
    # return redirect("users:user_profile", username=user.username)


@login_required(login_url="/accounts/login/")
def profile_unfollow(request, username):
    user = get_object_or_404(User, username=username)

    if request.user.is_authenticated and (request.user != user):
        # Check if current user is following `user`
        following = user.followers.filter(follower_id=request.user.id)

        if not following:
            return redirect(request.META.get("HTTP_REFERER"))

        # Unfollow user
        following.delete()

    # Return back to user's profile
    return redirect(request.META.get("HTTP_REFERER"))
