from django import forms
from ForumApp.models import CommentForum


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentForum
        fields = ('comment',)
