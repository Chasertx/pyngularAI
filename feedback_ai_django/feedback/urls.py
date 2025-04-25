#Purpose: App-level routing — connects URLs to views.
from django.urls import path
from .views import submit_feedback, summarize_feedback, get_all_summaries, get_feedback

urlpatterns = [
    path('feedback/', submit_feedback),
    path('story/summarizer/', summarize_feedback),
    path('stories/', get_all_summaries),
    path('feedback/everything/', get_feedback),
]