from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from ckeditor.fields import RichTextField


class Topic(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("topic-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    cover_image = models.ImageField(upload_to="covers/")
    body = RichTextField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, related_name="posts")
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title
