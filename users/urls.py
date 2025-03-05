from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("profile/<str:username>/", views.profile_view, name="user_profile"),
    path("profile/<str:username>/edit/", views.profile_edit, name="edit_profile"),
    path("follow/<str:username>/", views.profile_follow, name="follow_user"),
    path("unfollow/<str:username>/", views.profile_unfollow, name="unfollow_user"),
]
