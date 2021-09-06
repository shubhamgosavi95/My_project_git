import boards
from os import name, truncate
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = "board"

    def __str__(self):
        return self.name

    def get_post_count(self):
        return Post.objects.filter(topic__board = self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board = self).order_by("-created_at").first()

class Topic(models.Model):
    subject = models.CharField(max_length=300)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name="topics", on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name="topics", on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = "topic"

    def __str__(self):
        return self.subject

# to get topic from board(related name is given)
# Board.topics.all()  ----   (because are many)
# related name is not given then - Board.topic_set.all()

# to get board from topic
# Topic.board     ---- (because board is one (one to many relation))


class Post(models.Model):
    message = models.TextField(max_length=5000)
    topic = models.ForeignKey(Topic, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name="+", on_delete=models.CASCADE)

    class Meta:
        db_table = "post"

# to fetch post from topic
# t1.posts.all()
# Post.objects.filter(topic__board=board)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
