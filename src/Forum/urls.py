from django.urls import path
from . import views
from .views import (ThreadListView,
	ThreadDetailView,
	ThreadCreateView,
	ThreadDeleteView,
	ThreadUpdateView

	)

urlpatterns = [
	path('', ThreadListView.as_view(),name='thread-home'),
    path('<int:pk>/', ThreadDetailView.as_view(),name='thread-detail'),
    path('new/',ThreadCreateView.as_view(),name = 'thread-create'),
    path('<int:pk>/delete', ThreadDeleteView.as_view(),name='thread-delete'),
    path('<int:pk>/update', ThreadUpdateView.as_view(),name='thread-update'),
]