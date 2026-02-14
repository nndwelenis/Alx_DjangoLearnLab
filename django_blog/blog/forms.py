from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Comment
from .models import Post

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')

        if not content:
            raise forms.ValidationError("Comment cannot be empty.")

        if len(content) < 3:
            raise forms.ValidationError("Comment must be at least 3 characters long.")

        return content