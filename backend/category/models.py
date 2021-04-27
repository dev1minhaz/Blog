from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(blank=False, max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"

    def __str__(self):
        return self.name
