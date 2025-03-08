from django.contrib import admin
from .models import BlogPost, Tag, Category, Like, Comment, Save, ReadingHistory


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("created_at", "tags", "category")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    list_filter = ("created_at",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("user", "created_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("user", "created_at")
    search_fields = ("content",)


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("user", "created_at")

@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("user", "created_at")
