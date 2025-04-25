from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback, StorySummarization
from .serializers import FeedbackSerializer, StorySummarizationSerializer
from .ai import analyze_sentiment, summarize_text

@api_view(['POST'])
def submit_feedback(request):
    
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

# api/feedback/everything
@api_view(['GET'])
def get_feedback(request):
        # Handle GET request: Return all feedback entries
    feedback = Feedback.objects.all()
    serializer = FeedbackSerializer(feedback, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#Post /api/feedback/summary/
@api_view(['POST'])
def summarize_feedback(request):
    print("Raw Request Data:", request.body) # Debug: see raw payload
    print("Parsed Request Data:", request.data) # Debug: see parsed JSON
    

    text = request.data.get("text")
    if not text:
        return Response({"error": "Text field is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    summary = summarize_text(text)

    #save to database
    story = StorySummarization.objects.create(text=text, summary=summary)


    return Response({"summary": summary, "id": story.id}, status=status.HTTP_200_OK)

#api/stories
@api_view(['GET'])
def get_all_summaries(request):
    stories = StorySummarization.objects.all().order_by('-created_at')
    serializer = StorySummarizationSerializer(stories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)