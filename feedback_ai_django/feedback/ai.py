from transformers import pipeline

# Load sentiment analysis pipeline from Hugging Face
# Explicitly specify the model and revision
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)
# Analyze text and return a sentiment label (POSITIVE, NEGATIVE, etc.)
def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using a pre-trained model.
    Returns a string label like 'POSITIVE' or 'NEGATIVE'.
    """
    result = sentiment_pipeline(text)[0]
    return result["label"]