from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Comment
from .models import Post, Tag

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
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
    

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

        tag_names = self.cleaned_data.get('tags')
        if tag_names:
            tag_list = [name.strip() for name in tag_names.split(',')]

            post.tags.clear()

            for name in tag_list:
                tag, created = Tag.objects.get_or_create(name=name)
                post.tags.add(tag)

        return post
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['tags'].initial = ', '.join(
                tag.name for tag in self.instance.tags.all()
            )



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