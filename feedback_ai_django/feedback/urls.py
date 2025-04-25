#Purpose: App-level routing — connects URLs to views.
from django.urls import path
from .views import submit_feedback

urlpatterns = [
    path('feedback/', submit_feedback),
]