from django.db import models

# Represents user feedback stored in the database.
class Feedback(models.Model):
    text = models.TextField()# User-submitted feedback
    sentiment = models.CharField(max_length=50)# Sentiment from AI model
    category = models.CharField(max_length=100, default="General") # Optional categorization
    temp_field = models.BooleanField(default=False)  # Temporary field for migration

    def __str__(self):
        # Makes admin panel and shell easier to read
        return f"{self.text[:30]}... - ({self.sentiment})"
    

class StorySummarization(models.Model):
    text = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"StorySummary #{self.id}"