from django.db import models
from App_Login.models import User
# Create your models here.


class Forum(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='forum_author')
    forum_title = models.CharField(
        max_length=264, verbose_name='Put a Title')
    slug = models.SlugField(max_length=264, unique=True)
    forum_content = models.TextField(verbose_name="write your problem")
    forum_image = models.ImageField(
        upload_to='forum_images', verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_data = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-publish_date',)

    def __str__(self):
        return self.forum_title


class CommentForum(models.Model):
    forum = models.ForeignKey(
        Forum, on_delete=models.CASCADE, related_name='forum_comment')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='forum_user_comment')

    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-comment_date',)

    def __str__(self):
        return self.comment
