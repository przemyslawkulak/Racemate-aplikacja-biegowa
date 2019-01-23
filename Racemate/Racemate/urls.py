"""Racemate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path

from racemate.views import (Index, LogoutView, LoginView, LandingView, RunningGroupView, MemberView, ForumView, \
                            AddTrainingView, SendMessageView, LandingGeneratorView, MessangerView, AddTreningView,
                            TreningPlanView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('start/', LandingView.as_view(), name='landing-page'),
    re_path(r'start/(?P<id>(\d)+)/$', LandingGeneratorView.as_view(), name='landing-pages'),
    re_path(r'running_group/(?P<id>(\d)+)/$', RunningGroupView.as_view(), name='running-group'),
    re_path(r'member/(?P<id>(\d)+)/$', MemberView.as_view(), name='member'),
    re_path(r'forum/(?P<id>(\d)+)/$', ForumView.as_view(), name='forum'),
    path('add_training/', AddTrainingView.as_view(), name='addtraining'),
    path('send_message/', SendMessageView.as_view(), name='sendmessage'),
    re_path('messanger/(?P<id>(\d)+)/$', MessangerView.as_view(), name='messanger'),
    path('add_plan/', AddTreningView.as_view(), name='addplan'),  # nie zrobione
    path('treningplan/', TreningPlanView.as_view(), name='plan'),  # nie zrobione

]
