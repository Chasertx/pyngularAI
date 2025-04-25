from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback
from .serializers import FeedbackSerializer
from .ai import analyze_sentiment

@api_view(['GET','POST'])
def submit_feedback(request):
    if request.method == 'GET':
        # Handle GET request: Return all feedback entries
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        print("Raw Request Data:", request.body) # Debug: see raw payload
        print("Parsed Request Data:", request.data) # Debug: see parsed JSON

        # Extract 'text' field from request body
        text = request.data.get("text")
        # If no text provided, return an error
        if not text:
            return Response({"error": "Text field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Use AI model to analyze sentiment
        sentiment = analyze_sentiment(text)
        # Save to database
        feedback = Feedback.objects.create(text=text, sentiment=sentiment)
        # Serialize and return the new object
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
