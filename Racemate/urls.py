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

from calc.views import CalculatorView
from group.views import RunningGroupView, MemberView, CreateGroupView, ShowGroupsView, JoinGroupView, JoinConfirmView, \
    AdminConfirmView, AdminView
from messanger.views import ForumView, ForumChoiceView, SendMessageView, SendMessageGroupView, MessangerView
from racemate.views import (LogoutView, LoginView, LandingView, LandingGeneratorView,
                            RegisterView, customhandler404, customhandler500)
from training.views import AddTrainingView, AddTreningView, TreningPlanWhiteView, TreningPlan18weeksView, \
    LoadTreningView, PlanChoiceView, DeleteTrainingView, PastTrainingDelete

handler404 = customhandler404
handler500 = customhandler500

urlpatterns = [

    # racemate
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', LandingView.as_view(), name='landing-page'),
    re_path(r'start/(?P<id>(\d)+)/$', LandingGeneratorView.as_view(), name='generate_vdot'),

    # group
    re_path(r'running_group/(?P<id>(\d)+)/$', RunningGroupView.as_view(), name='running-group'),
    re_path(r'member/(?P<id>(\d)+)/$', MemberView.as_view(), name='member'),
    path('creategroup/', CreateGroupView.as_view(), name='create-group'),
    path('showgroups/', ShowGroupsView.as_view(), name='show-groups'),
    path('joingroup/', JoinGroupView.as_view(), name='join-group'),
    re_path(r'joingroupconfirm/(?P<id>(\d)+)/$', JoinConfirmView.as_view(), name='join-group-confirm'),
    re_path(r'adminconfirm/(?P<id>(\d)+)/(?P<sender>(\d)+)$', AdminConfirmView.as_view(), name='adminconfirm'),
    re_path(r'adminview/(?P<id>(\d)+)$', AdminView.as_view(), name='adminview'),

    # messanger
    re_path(r'forum/(?P<id>(\d)+)/$', ForumView.as_view(), name='forum'),
    path('forumchoice', ForumChoiceView.as_view(), name='forum-choice'),
    path('send_message/', SendMessageView.as_view(), name='sendmessage'),
    path('send_message_group', SendMessageGroupView.as_view(), name='sendmessagegroup'),
    re_path(r'^messanger/(?P<id>(\d)+)/$', MessangerView.as_view(), name='messanger'),

    # training
    path('add_training/', AddTrainingView.as_view(), name='addtraining'),
    path('add_plan/', AddTreningView.as_view(), name='addplan'),  # nie zrobione
    path('treningplan_white/', TreningPlanWhiteView.as_view(), name='whiteplan'),
    path('treningplan_18weeks/', TreningPlan18weeksView.as_view(), name='18weeksplan'),
    path('loadtrening/', LoadTreningView.as_view(), name='loadtrening'),
    path('planchoice/', PlanChoiceView.as_view(), name='planchoice'),
    re_path(r'^deletetraining/(?P<id>(\d)+)/$', DeleteTrainingView.as_view(), name='deletetraining'),
    re_path(r'^(?P<pk>\d+)/delete/$', PastTrainingDelete.as_view(), name='delete'),

    #calc
    path('calculator/', CalculatorView.as_view(), name='calculator')
]