#Converts between Python objects and JSON (used by the API).
from rest_framework import serializers
from .models import Feedback, StorySummarization

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'text', 'sentiment', 'category']

class StorySummarizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorySummarization
        fields = '__all__'