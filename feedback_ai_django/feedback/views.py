from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback, StorySummarization
from .serializers import FeedbackSerializer, StorySummarizationSerializer
from .ai import analyze_sentiment, summarize_text
from django.apps import apps
from django.forms.models import model_to_dict
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

#Endpoint: api/feedback
#Handles submission of feedback for sentiment analysis.
@api_view(['POST'])
def submit_feedback(request):
    
    if request.method == 'POST':
        # Extract 'text' field from request body
        text = request.data.get("text")
        # If no text provided, return an error
        if not text:
            return Response({"error": "Text field is required."}, status=status.HTTP_400_BAD_REQUEST)

        #use the ai.py service to analyze the sentiment of the text.
        sentiment = analyze_sentiment(text)

        #Create and save a new Feedback record in the database.
        feedback = Feedback.objects.create(text=text, sentiment=sentiment)

        # Serialize the feedback object to JSON format for the response.
        serializer = FeedbackSerializer(feedback)
        #Return the serialized data with a 201 created status.
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# api/feedback/everything
@api_view(['GET'])
def get_feedback(request):
    #Query all feedback records from the database.
    feedback = Feedback.objects.all()
    #Serialize the feedback queryset (true for multiple records).
    serializer = FeedbackSerializer(feedback, many=True)
    #return the serialized data a 200 ok status.
    return Response(serializer.data, status=status.HTTP_200_OK)

#Post /api/story/summarizer
@api_view(['POST'])
def summarize_feedback(request):
    print("Raw Request Data:", request.body) # Debug: see raw payload
    print("Parsed Request Data:", request.data) # Debug: see parsed JSON
    
    # Extract 'text' field from request body
    text = request.data.get("text")
    # If no text provided, return an error.
    if not text:
        return Response({"error": "Text field is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    #generate a summary using the ai.py summarize function.
    summary = summarize_text(text)

    #create and save a new story summarization record in the database.
    story = StorySummarization.objects.create(text=text, summary=summary)

    #return the summary and the new record's ID with a 200 ok status.
    return Response({"summary": summary, "id": story.id}, status=status.HTTP_200_OK)

#api/stories
@api_view(['GET'])
def get_all_summaries(request):
    #Query the story summarization records ordered from newest to oldest.
    stories = StorySummarization.objects.all().order_by('-created_at')
    #Serialize the queryset (true for multiple records).
    serializer = StorySummarizationSerializer(stories, many=True)
    #return the serialized data with a 200 ok status.
    return Response(serializer.data, status=status.HTTP_200_OK)

#api/databasevisualizer
@api_view(['GET'])
def get_all_tables(request):
    #Extract query parameters from the request.
    model_name = request.query_params.get('model')
    search = request.query_params.get('search', '').strip()
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))

    #Validate that the model name is provided. return 400 error if it's missing.
    if not model_name:
        return Response({"error": "Please provide a model name (?model=ModelName)."},status=status.HTTP_400_BAD_REQUEST)

    #Get the model class from the 'feedback' app.
    try:
        model = apps.get_model('feedback', model_name)
    except LookupError:
        #Return this error if model is not found in the app.
        return Response({"error": f"Model '{model_name}' not found."}, status=status.HTTP_404_NOT_FOUND)
    
    #Start with all records of the model.
    queryset = model.objects.all()

    #If a search term is provided, filter the queryset based on it.
    if search:
        #Identify charfield and text fields for searching.
        search_fields = [f.name for f in model._meta.fields if f.get_internal_type() in ['CharField', 'TextField']]
        #Build a Q object for OR-based search across text fields.
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": search})
        #Filter the queryset using the q object.
        queryset = queryset.filter(q_objects)
    
    #Get the total count of records in the query set.
    total = queryset.count()

    #Setting up pagination.
    start = (page - 1) * page_size
    end = start + page_size
    paginated = queryset[start:end]

    #converting paginated objects to dictionaries.
    data = [model_to_dict(obj) for obj in paginated]

    #Return the response with model name, total count, current page, page size, and the paginated results.
    return Response({
        "model": model_name,
        "count": total,
        "page": page,
        "page_size": page_size,
        "results": data,
    })

#api/contact endpoint
@api_view(['POST'])
def contact_view(request):
    print("Raw Request Data:", request.body) # Debug: see raw payload
    print("Parsed Request Data:", request.data) # Debug: see parsed JSON
    
    #Extract 'name', 'email', and 'message' fields from request body.
    name = request.data.get('name')
    email = request.data.get('email')
    message = request.data.get('message')

    
    #Validate that all fields are provided. return 400 error if any field is missing.
    if not name or not email or not message:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    #Prepare the email subject and body.
    subject = f"New Contact Message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"


    try:
        #Send the email using django's sendmail function (we used a custom email backend).
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
        #return success message.
        return Response({'message': 'Email sent successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)