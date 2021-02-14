from django.urls import path
from . import views
from .views import (TaskListView,
	TaskCreateView,
	TaskUpdateView,
	TaskDeleteView

    )

urlpatterns = [
    path('', TaskListView.as_view(),name='task-home'),
    path('new/', TaskCreateView.as_view(),name='task-create'),
    path('<int:pk>/update', TaskUpdateView.as_view(),name='task-update'),
    path('<int:pk>/delete', TaskDeleteView.as_view(),name='task-delete'),
    #
]