from django import forms
from django.shortcuts import get_object_or_404
from .models import Post, PostLike, PostComment

class CreatePostForm(forms.Form):
    title   = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)