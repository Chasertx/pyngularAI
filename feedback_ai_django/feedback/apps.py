from django.apps import AppConfig

# Defining the config class for the app.
class FeedbackConfig(AppConfig):
    #Default field type for auto-generated primary keys in the model. 
    default_auto_field = 'django.db.models.BigAutoField'
    #App name.
    name = 'feedback'
