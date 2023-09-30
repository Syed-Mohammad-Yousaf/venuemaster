from django.db import models
from django.utils.text import slugify


class SlugModel(models.Model):
    slug = models.SlugField(unique=True, max_length=500)

    class Meta:
        abstract = True

    def generate_slug(self):
        self.slug = slugify(str(self))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.generate_slug()

        return super().save(*args, **kwargs)
