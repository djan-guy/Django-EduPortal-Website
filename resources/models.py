from django.db import models
from django.utils.text import slugify

class Resource(models.Model):
    title = models.CharField(max_length=75)
    file = models.CharField()
    course = models.CharField(default="Course")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
