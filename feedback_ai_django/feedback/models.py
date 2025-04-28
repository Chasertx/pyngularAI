from django.db import models

# Represents user feedback stored in the database.
class Feedback(models.Model):
    # Textfield to store the user-submitted feedback.
    text = models.TextField()
    # Charfield to store the sentiment (positive or negative).
    sentiment = models.CharField(max_length=50)
    # Charfield for an optional category.
    category = models.CharField(max_length=100, default="General") 
    # this is just for migration purposes, it will be deleted later.
    temp_field = models.BooleanField(default=False)  

    def __str__(self):
        """
        String representation of the Feedback instance for better readability
        in the Django admin panel and shell.
        Returns:
            str: First 30 characters of feedback text followed by sentiment.
        """
        return f"{self.text[:30]}... - ({self.sentiment})"
    
# Model to store story summaries.
class StorySummarization(models.Model):
    # Textfield to store the original story text.
    text = models.TextField()
    # Textfield to store the summarized version of the story.
    summary = models.TextField()
    # DateTimeField to store when the summary was created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the StorySummarization instance for better readability
        in the Django admin panel and shell.
        Returns:
            str: A string indicating the summary's ID.
        """
        return f"StorySummary #{self.id}"