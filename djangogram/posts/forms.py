from socket import fromshare
from django import forms
from .models import Post, Comment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "image"]

        labels = {
            "caption": "내용",
            "image": "사진"
        }

class CommentForm(forms.ModelForm):
    contents = forms.CharField(widget=forms.Textarea, label="")
    # 레이블을 지워주기 위해 추가

    class Meta:
        model = Comment
        fields = ["contents"]

        labels = {
            "contents": "내용",
        }

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]