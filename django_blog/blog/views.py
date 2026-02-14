from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm
from .forms import UserRegisterForm

# For CRUD operations
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post

from .forms import PostForm

# For Comments
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import Post, Comment
from .forms import CommentForm

#Search functinality
from django.db.models import Q
from .models import Tag

# Create your views here.

def home(request):
    return render(request, 'blog/base.html')

def posts(request):
    return render(request, 'blog/base.html')

def register(request):
    return render(request, 'blog/base.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})



class PostListView(ListView):  #This shows all posts.
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):   #This allows logged-in users to create posts.
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   #That form_valid method attaches the logged-in user as author.

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):    #Only the author must edit. 
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):   #Only the author can delete. 
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.post.get_absolute_url()


def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.none()

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'results': results
    }

    return render(request, 'blog/search_results.html', context)



def posts_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    posts = tag.posts.all()

    context = {
        'tag': tag,
        'posts': posts
    }

    return render(request, 'blog/posts_by_tag.html', context)
