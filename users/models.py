from django.db import models
from accounts.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)  # Supports Markdown
    profile_picture = models.ImageField(
        upload_to="user_profiles/",
        null=True,
        blank=True,
    )
    profile_banner = models.ImageField(
        upload_to="profile_banners/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.fullname or self.user.username


# Following system
class Subscription(models.Model):
    # The one following
    follower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="followings",  # Name in User model (Follower in this model is following in user model)
    )
    # The one being followed (So confusing in here)
    following = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="followers",  # Name in User model
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} is following {self.following}"
