from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import DeleteView

import boards

from .forms import NewTopicForm, PostForm
from .models import Board, Post, Topic
from django.db.models import Count

# Create your views here.


def home(request):
    # boards = Board.objects.all()
    # boards_names = []

    # for board in boards:
    #     boards_names.append(board.name)

    # response_html = '<br>'.join(boards_names)
    # # print(response_html)

    return render(request, "home.html", context={"all_boards":Board.objects.all()})

@login_required
def board_topics(request, pk):
    # try:
    #     board_obj = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404
    board_obj = get_object_or_404(Board, pk=pk)
    topics = board_obj.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, "topics.html", {"board": board_obj, "all_topics":topics})

# def new_topic(request, pk):
#     board_obj = get_object_or_404(Board, pk=pk)
#     if request.method == 'POST':
#         subject = request.POST["subject"]
#         message = request.POST["message"]

#         user = User.objects.first()    # TODO: get the currently logged in user

#         topic = Topic.objects.create(
#             subject = subject,
#             board = board_obj, 
#             starter = user
#         )

#         post = Post.objects.create(
#             message = message,
#             topic = topic,
#             created_by = user
#         )

#         return redirect("board_topics", pk=board_obj.pk)  # TODO: redirect to the created topic page

#     return render(request, "new_topic.html", {"board": board_obj})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    # print(request.user)                 # ---- here we getting users object
    # user = User.objects.first()  # TODO: get the currently logged in user  --- use first user 
    user = request.user         # topic will created by login user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('topic_posts', pk=board.pk, topic_pk=topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.user:
        
        pass
    else:
        topic.views += 1
        topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

# funtion based view
@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

from django.views.generic import View


# class based view

# class NewPostView(View):
#     def render(self, request, context):
#         return render(request, 'new_post.html', context)

#     def post(self, request, **kwargs):
#         topic = get_object_or_404(Topic, board__pk=kwargs["pk"], pk=kwargs["topic_pk"])
#         self.form = PostForm(request.POST)
#         if self.form.is_valid():
#             post = self.form.save(commit=False)
#             post.topic = topic
#             post.created_by = request.user
#             post.save()
#             self.form.save()
#             return redirect('topic_posts', pk=kwargs["pk"], topic_pk=kwargs["topic_pk"])
#         return self.render(request)

#     def get(self, request, **kwargs):
#         self.form = PostForm()
#         topic = get_object_or_404(Topic, board__pk=kwargs["pk"], pk=kwargs["topic_pk"])
#         return self.render(request, context= {'form': self.form, "topic":topic})

# Generic class based view

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name = 'new_post.html'


    def post(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, board__pk=kwargs["pk"], pk=kwargs["topic_pk"])
        self.form = PostForm(request.POST)
        if self.form.is_valid():
            post = self.form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            self.form.save()
            return redirect('topic_posts', pk=kwargs["pk"], topic_pk=kwargs["topic_pk"])

def func():
    pass