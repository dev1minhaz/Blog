from tag.models import Tag
from django.db import models
from category.models import Category
from django.contrib.auth import get_user_model
User = get_user_model()


def blog_img_path(instance, filename):
    return 'blog_images/{0}/{1}'.format(instance.author.username, filename)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=264, unique=True)
    blog_content = models.TextField()
    image = models.ImageField(upload_to=blog_img_path)
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_draft = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-publish_date', ]

    def __str__(self):
        return f"id: {self.id}, author: {self.author}, title: {self.title}"

    @property
    def comments_list(self):
        return self.comments.filter(is_hidden=False)
