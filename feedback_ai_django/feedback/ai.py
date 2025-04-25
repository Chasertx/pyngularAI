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

#Load Summarizer once (using BART model)
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

def summarize_text(text):
    if len(text.split()) < 30:
        return "input too short to summarize"
    
    summary = summarizer(text, max_length=60, min_length=25, do_sample=False)
    return summary[0]['summary_text']