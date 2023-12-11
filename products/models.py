from django.db import models
from django.template.defaultfilters import slugify
import os
from tinymce.models import HTMLField
from categories.models import Categories
from django.urls import reverse
from django.db.models import Count, Avg
from django.contrib.auth import get_user_model
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
                             unique=False, blank=False)
    price = models.IntegerField(default=0, blank=False)
    offer_price = models.IntegerField(default=0, blank=True)
    discount_applied = models.BooleanField(default=False)
    old_price = models.IntegerField(default=0, blank=True)
    percentage = models.CharField(max_length=100, default="", blank=True)
    stock = models.IntegerField(blank=False)
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

        if not self.discount_applied and self.offer_price > 0:
            print(type(self.offer_price))
            actual_price = self.price
            new_price = (self.price - self.offer_price)
            self.price = new_price
            self.old_price = actual_price
            percentage = (self.offer_price / self.price) * 100
            self.percentage = f"{percentage:.0f}%"
            self.discount_applied = True
            print("Precio", self.price)
            print("Precio viejo", self.old_price)
        super().save(*args, *kwargs)

    def get_url(self):
        return reverse("product_detail", args=[self.series.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewProduct.objects.filter(
            product=self, status=True).aggregate(average=Avg("rating"))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def countReview(self):
        reviews = ReviewProduct.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class ReviewProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment: {self.user}"
