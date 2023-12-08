from django.db import models
import datetime
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
import os
from products.models import Product
# Create your models here.


class Carousel(models.Model):
    def image_upload_to(self, instance):
        if instance:
            return os.path.join("Carousel_images/", instance)
        return None

    def validate_image_count(self):
        image_count = Carousel.objects.all().count()
        if image_count >= 3:
            raise ValidationError(
                "Only three images can be selected. If you need to change select image, you need to delete one select image and select the new image ")
    title = models.CharField(max_length=100, default="", blank=False)
    slogan = models.CharField(max_length=300, blank=False, unique=False)
    series = models.ForeignKey(
        Product, default="", blank=False, on_delete=models.CASCADE, help_text="Select a product to post in the carousel", validators=[validate_image_count])
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Upload images for carousel"
        db_table = "Images_Carousel"

    def __str__(self):
        return self.title
