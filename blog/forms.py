from django import forms

from .models import Post, PostComment


class CreatePostForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
        )


class CommentForm(forms.Form):
    comment = forms.CharField(label="")

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["placeholder"] = "Comment"


class UpdateCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ("comment",)
