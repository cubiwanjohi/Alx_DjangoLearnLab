from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


# -----------------------
# COMMENT FORM
# -----------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Add a comment...'}
            )
        }


# -----------------------
# USER REGISTRATION FORM
# -----------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# -----------------------
# POST FORM WITH TAGS
# -----------------------
class PostForm(forms.ModelForm):

    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas (e.g. django, python, web)",
        widget=forms.TextInput(attrs={'placeholder': 'django, python, web'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # author set automatically