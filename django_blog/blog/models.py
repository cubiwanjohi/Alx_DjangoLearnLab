from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# -----------------------
# TAG MODEL
# -----------------------
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# -----------------------
# BLOG POST MODEL
# -----------------------
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    # MANY-TO-MANY RELATIONSHIP WITH TAGS
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    def __str__(self):
        return self.title

    # Redirect after create/update/delete
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


# -----------------------
# COMMENT MODEL
# -----------------------
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # Oldest comments first

    def __str__(self):
        return f'Comment by {self.author.username} on "{self.post.title}"'

    def get_absolute_url(self):
        return self.post.get_absolute_url()