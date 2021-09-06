"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from boards import views
from django.conf.urls import url

from accounts import views as accounts_view
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),  # r - regex -regular expresion, ^ - carrot - starts with nothing, $ - dollar - ends with nothing 
    # path("", views.home, name="home") 
    url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),

    # account urls

    url(r'^signup/$', accounts_view.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),     # Django's class based view so thats why - as_view()
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # reset password

    url(r'^reset/$', auth_views.PasswordResetView.as_view(template_name='password_reset.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt'), name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,100})/$', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
  
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
   url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),


    # Class based view
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/new_post/$', views.NewPostView.as_view(), name='new_post'),

]


# http://127.0.0.1:8000/admin/
# http://127.0.0.1:8000/  - (use when r'^$  - (start with nothing ends with nothing))

# http://127.0.0.1:8000/boards/
# http://127.0.0.1:8000/boards/pk(int)/new
