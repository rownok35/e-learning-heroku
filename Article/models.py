from django.db import models
from App_Login.models import User
# Create your models here.


class Article_model(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post_author')
    article_title = models.CharField(
        max_length=264, verbose_name='Put a Title')
    slug = models.SlugField(max_length=264, unique=True)
    article_content = models.TextField(verbose_name="What is on your mind?")
    article_image = models.ImageField(
        upload_to='article_images', verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_data = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-publish_date',)

    def __str__(self):
        return self.article_title


class Comment(models.Model):
    article = models.ForeignKey(
        Article_model, on_delete=models.CASCADE, related_name='article_comment')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_comment')

    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-comment_date',)

    def __str__(self):
        return self.comment


class Likes(models.Model):
    article = models.ForeignKey(
        Article_model, on_delete=models.CASCADE, related_name='liked_article')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liker_user')

    def __str__(self):
        return self.user + ' likes ' + self.article
