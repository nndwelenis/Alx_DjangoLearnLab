from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import PostByTagListView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Blog Post CRUD
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comment URLs
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # Search
    path('search/', views.search_posts, name='search'),

    # Tag-based filtering
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),





]
