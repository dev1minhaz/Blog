from django.db import models
from django.template.defaultfilters import truncatechars
from post.models import Post
from django.contrib.auth import get_user_model
User = get_user_model()


class Comment(models.Model):
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, blank=False, null=False, on_delete=models.CASCADE)

    @property
    def short_description(self):
        return truncatechars(self.content, 100)
