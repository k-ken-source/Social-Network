from django.urls import path
from . import views
from .views import (PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView, 
	PostDeleteView,
	UserPostListView, 

	BlogListView,
	BlogCreateView,
	BlogDetailView,
	BlogUpdateView,
    BlogDeleteView
	)

urlpatterns = [
    path('', PostListView.as_view(),name='blog-home'),
    path('blog/', BlogListView.as_view(),name='blog'),

    path('post/<int:pk>/', PostDetailView.as_view(),name='post-detail'),
    path('blog/<int:pk>/', BlogDetailView.as_view(),name='blog-detail'),

    path('post/new', PostCreateView.as_view(),name='post-create'),
    path('blog/new', BlogCreateView.as_view(),name='blog-create'),

    path('post/<str:username>', UserPostListView.as_view(),name='user-posts'),

    path('post/<int:pk>/update', PostUpdateView.as_view(),name='post-update'),
    path('blog/<int:pk>/update', BlogUpdateView.as_view(),name='blog-update'),

    path('post/<int:pk>/delete', PostDeleteView.as_view(),name='post-delete'),
    path('blog/<int:pk>/delete', BlogDeleteView.as_view(),name='blog-delete'),
    #path('about/', views.about,name='blog-about'),
    path('like', views.likePost,name='LikePost'),


]
