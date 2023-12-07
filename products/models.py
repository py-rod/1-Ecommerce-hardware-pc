from django.db import models
from django.template.defaultfilters import slugify
import os
from tinymce.models import HTMLField
from categories.models import Categories
from django.urls import reverse
# Create your models here.


class Product(models.Model):
    def image_upload_to(self, instance):
        if instance:
            return os.path.join("Products_images", slugify(self.product_name), instance)
        return None

    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=False)
    description = HTMLField(default="", blank=False)
    brand = models.CharField(max_length=200, default="",
                             unique=True, blank=False)
    price = models.IntegerField(default=0, blank=False)
    offer_price = models.IntegerField(default=0, blank=True)
    old_price = models.IntegerField(default=0, blank=True)
    percentage = models.CharField(max_length=100, default="", blank=True)
    stock = models.IntegerField(default=0, blank=False)
    image = models.ImageField(
        default="./default/placeholder.webp", upload_to=image_upload_to, max_length=5000)
    series = models.ForeignKey(Categories, default="", blank=False,
                               help_text="Select the category to which this product belongs", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if self.offer_price > 0:
            actual_price = self.price
            new_price = (self.price - self.offer_price)
            self.price = new_price
            self.old_price = actual_price
            percentage = (self.offer_price / self.price) * 100
            self.percentage = f"{percentage:.0f}%"
            super().save(*args, *kwargs)
        else:
            self.old_price = 0
            self.percentage = ""
            super().save(*args, *kwargs)

    def get_url(self):
        return reverse("product_detail", args=[self.series.slug, self.slug])

    def __str__(self):
        return self.product_name
