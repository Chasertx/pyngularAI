#Converts between Python objects and JSON (used by the API).
from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'text', 'sentiment', 'category']
