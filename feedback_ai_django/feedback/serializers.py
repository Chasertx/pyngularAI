#Converts between Python objects and JSON (used by the API).
from rest_framework import serializers
from .models import Feedback, StorySummarization

# Serializer for the feedback model. 
# Handles serialization and deserialization.
class FeedbackSerializer(serializers.ModelSerializer):
    # Configure the serializer's behavior.
    class Meta:
        # The model to be serialized.
        model = Feedback
        # Fields to include in the serialized output.
        fields = ['id', 'text', 'sentiment', 'category']

# Serializer for the story summarization model.
# Handles serialization and deserialization.
class StorySummarizationSerializer(serializers.ModelSerializer):
    # Configure the serializer's behavior.
    class Meta:
        # Model to be serialized.
        model = StorySummarization
        # Include all fields in the serialized output.
        fields = '__all__'