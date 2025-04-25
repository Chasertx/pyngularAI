from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback, StorySummarization
from .serializers import FeedbackSerializer, StorySummarizationSerializer
from .ai import analyze_sentiment, summarize_text
from django.apps import apps
from django.forms.models import model_to_dict
from django.db.models import Q

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

#api/databasevisualizer
@api_view(['GET'])
def get_all_tables(request):
    model_name = request.query_params.get('model')
    search = request.query_params.get('search', '').strip()
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))

    if not model_name:
        return Response({"error": "Please provide a model name (?model=ModelName)."},status=status.HTTP_400_BAD_REQUEST)

    #get model class dynamicall from app 
    try:
        model = apps.get_model('feedback', model_name)
    except LookupError:
        return Response({"error": f"Model '{model_name}' not found."}, status=status.HTTP_404_NOT_FOUND)
    
    #prepare query set
    queryset = model.objects.all()

    #optional keyword filtering (searches all charffields/textfields)
    if search:
        search_fields = [f.name for f in model._meta.fields if f.get_internal_type() in ['CharField', 'TextField']]
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": search})
        queryset = queryset.filter(q_objects)
    
    total = queryset.count()

    #Pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated = queryset[start:end]

    data = [model_to_dict(obj) for obj in paginated]

    return Response({
        "model": model_name,
        "count": total,
        "page": page,
        "page_size": page_size,
        "results": data,
    })