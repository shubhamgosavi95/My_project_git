from django.apps import AppConfig

# added new line from git 
class BoardsConfig(AppConfig):
    """This is boards configuretion"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boards'
