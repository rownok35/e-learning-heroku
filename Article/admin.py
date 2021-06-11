from django.contrib import admin
from Article.models import Article_model, Likes, Comment
# Register your models here.

admin.site.register(Article_model)
admin.site.register(Likes)
admin.site.register(Comment)
