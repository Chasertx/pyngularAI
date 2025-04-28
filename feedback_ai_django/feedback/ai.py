#Import the pipeline function from the transformer library
from transformers import pipeline

#Loading the sentiment analysis pipeline with the distilbert model.
#Model: distilbert-base-uncased-finetuned-sst-2-english
#Revision: specifies a specific version of the model.
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)

#This function takes a string and analyzes the sentiment (positive or negative).
def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using a pre-trained model.
    Args:
        text (str): The input text to analyze.
    Returns:
        str: Sentiment label ('POSITIVE' or 'NEGATIVE').
    """
    #Runs the text through the sentiment pipeline.
    result = sentiment_pipeline(text)[0]

    #Returns the sentiment label.(Positive or Negative).
    return result["label"]

#Loading up the summarization pipeline with the bar model.
#Model: BART large model. 
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

#This function takes a string input and returns a summarized version of the text.
def summarize_text(text):
    """
    Summarize the given text using a pre-trained BART model.
    Args:
        text (str): The input text to summarize.
    Returns:
        str: A summarized version of the text or an error message if input is too short.
    """
    #checking if the text is too short to summarize.
    if len(text.split()) < 30:
        return "input too short to summarize"
    
    # Generate a summary with specified length constraints
    # max_length: Maximum words in summary
    # min_length: Minimum words in summary
    # do_sample: Set to False for deterministic output
    summary = summarizer(text, max_length=60, min_length=25, do_sample=False)
    
    #Returning the summarized text.
    return summary[0]['summary_text']