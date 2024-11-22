from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here

# to create another custom manage class that returns all published posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)

    # By using unique_for_date, the slug field is now required
    # to be unique for the date stored in the publish field
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    #Post.published.all()  # Returns only published posts
    #Post.objects.all()  # Returns all posts

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    # This function for building canonical urls
    """
    The reverse() function will build the URL dynamically using the URL name defined
    in the URL paterns. We have used the blog namespace followed by a colon and
    the post_detail URL name. Remeber that the blog namespace is defined in the
    main urls.py file of the project when including the URL
    patterns from blog.urls. The post_detail URL is defined in the urls.py file of the blog application.mt
    """

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug]
        )


# The comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
                models.Index(fields=['created']),
            ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

