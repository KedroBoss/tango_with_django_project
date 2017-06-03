from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

CATEGORY_NAME_LENGTH = 128
PAGE_TITLE_LENGTH = 128

class Category(models.Model):
    name = models.CharField(max_length=CATEGORY_NAME_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique = True)

    # This will overide the default save method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=PAGE_TITLE_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):

    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    # upload_to goes to <MEDIA_ROOT> folder
    picture = models.ImageField(upload_to = 'profile_images', blank=True)

    def __str__(self):
        return self.user.username