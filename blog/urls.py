from django.urls import path
from . import views

# app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("explore/", views.explore, name="explore"),
    path("explore/category/<slug:slug>/", views.explore_category, name="explore_category"),
    path("explore/tag/<slug:slug>/", views.explore_tag, name="explore_tag"),
    # path("search/", views.search, name="search"),
    # CRUD
    path("blog/new/", views.create_post, name="create_post"),
    path("blog/<slug:slug>/edit/", views.edit_post, name="edit_post"),
    path("blog/<slug:slug>/delete/", views.delete_post, name="delete_post"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    # Like/Unlike
    path("blog/<slug:slug>/like/", views.like_post, name="like_post"),
    # Comments
    path("blog/<slug:slug>/comment/", views.comment_on_post, name="comment_on_post"),
    # Save Posts
    path("blog/<slug:slug>/save/", views.save_post, name="save_post"),
    path("blog/<slug:slug>/save/delete/", views.delete_saved, name="delete_saved"),
]
