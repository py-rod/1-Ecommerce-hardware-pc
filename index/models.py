from django.db import models
import datetime
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
import os
# Create your models here.


class Carousel(models.Model):
    def image_upload_to(self, instance):
        if instance:
            return os.path.join("Carousel_images/", instance)
        return None

    title = models.CharField(max_length=200, blank=False, unique=False)
    image = models.ImageField(
        default="./default/placeholder.webp", upload_to=image_upload_to, max_length=10000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Upload images for carousel"
        db_table = "Images_Carousel"

    def __str__(self):
        return self.title


class ImageCarouselSelect(models.Model):

    def validate_image_count(self):
        image_count = ImageCarouselSelect.objects.all().count()

        if image_count >= 3:
            raise ValidationError(
                "Only three images can be selected. If you need to change select image, you need to delete one select image and select the new image")

    series = models.ForeignKey(Carousel, default="", blank=False,
                               help_text="Select your images for see in the carousel", on_delete=models.CASCADE, validators=[validate_image_count])
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Select images for carousel"

    def __str__(self):
        return self.series.title
