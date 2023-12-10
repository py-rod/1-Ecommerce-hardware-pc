from django.db import models
from django.template.defaultfilters import slugify
import os
from django.urls import reverse
# Create your models here.


class Categories(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    slug = models.SlugField(unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("products_by_category", args=[self.slug])

    class Meta:
        verbose_name_plural = "Categories"
        db_table = "Categories"
