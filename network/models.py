from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="creator")
    content = models.CharField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} made by {self.user}"

class Following(models.Model):
    """
    follower - user who is following
    followed -  user being followed
    """
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")
    
    def __str__(self):
        return f"{self.follower} is following {self.followed}"
