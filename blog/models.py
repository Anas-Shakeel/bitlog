from django.db import models
from django.utils.text import slugify
from accounts.models import User


def get_default_category():
    """Returns the `ID` of default category `Uncategorized`"""
    return Category.objects.get_or_create(
        name="Uncategorized",
        slug="uncategorized",
    )[0].id


class BlogPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Mark as "Deleted User"
        null=True,
        related_name="posts",
    )
    cover_image = models.ImageField(upload_to="blog_covers/", null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    caption = models.CharField(max_length=300, blank=True, null=True)
    content = models.TextField()
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_DEFAULT,
        default=get_default_category,
        related_name="categorized_posts",
    )
    tags = models.ManyToManyField("Tag", blank=True, related_name="tagged_posts")
    view_count = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_unique_slug(self):
        """Generate a unique slug by apending a counter if needed"""
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if (
            not self.slug
            or self.title
            != BlogPost.objects.filter(pk=self.pk)
            .values_list("title", flat=True)
            .first()
        ):
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Tag(models.Model):
    # NAME, but as a SLUG
    name = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name = slugify(self.name, False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Commented on {self.post.title}"

    class Meta:
        ordering = ["-created_at"]


class Save(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete Saves if user is deleted
    )
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        null=True,
        related_name="saves",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Saved {self.post}"

class ReadingHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Delete <History> if user is deleted
    )
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        null=True,
        related_name="history",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Read {self.post}"
