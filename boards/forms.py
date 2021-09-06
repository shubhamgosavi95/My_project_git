from django import forms
from django.db.models import fields

from .models import Post, Topic

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is on your mind?'}), max_length=5000, help_text='The max length of the text is 5000.')
    
    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message',]







