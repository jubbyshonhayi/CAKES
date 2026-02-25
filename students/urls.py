from django.urls import path

from .views import (
    StudentCreateView,
    StudentDeleteView,
    StudentDetailView,
    StudentListView,
    StudentUpdateView,
)

urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('students/add/', StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/edit/', StudentUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
]
