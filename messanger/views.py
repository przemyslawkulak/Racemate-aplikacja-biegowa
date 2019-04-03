from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from racemate.forms import SendMessageForm, SendMessageGroupForm
from racemate.models import RunningGroup, MyUser, Message


class ForumView(LoginRequiredMixin, View):
    """
    View with all messages of one group and list of user group(with hyperlinks)
    """

    def get(self, request, id):
        group_forum = RunningGroup.objects.get(id=id)

        # all group members without user
        user = MyUser.objects.filter(members=group_forum).exclude(id=request.user.id)

        #  all group messages
        messages = Message.objects.filter(togroup=group_forum).order_by('-date_sent')

        #  group list
        groups = []
        admin = []
        group = RunningGroup.objects.all().filter(members=request.user)
        for i in group:
            admins = MyUser.objects.filter(admins=i)
            for j in admins:
                admin = j.username
            m = len(MyUser.objects.filter(members=i))
            groups.append({"name": i.name, "admins": admin, "members": m, "date": i.date, "id": i.id})
        return render(request, 'messanger/forum.html',
                      {'messages': messages, 'group': group_forum, "user": user, 'groups': groups})


class ForumChoiceView(LoginRequiredMixin, View):
    """
    View with list of all of user groups and all of user friends (with hyperlinks)
    """

    def get(self, request):

        # list of all user's group
        groups = []
        admin = []
        group = RunningGroup.objects.all().filter(members=request.user)
        for i in group:
            admins = MyUser.objects.filter(admins=i)
            for j in admins:
                admin = j.username
            m = len(MyUser.objects.filter(members=i))
            groups.append({"name": i.name, "admins": admin, "members": m, "date": i.date, "id": i.id})

        # list of all user's group
        friends = []
        group = RunningGroup.objects.filter(members=request.user)
        for i in group:
            friend = i.members.all()
            for j in friend:
                friends.append(j)

        # list of unread messeges
        unread_msg = Message.objects.filter(read=False).filter(to=request.user)

        return render(request, 'messanger/forumchoice.html',
                      {"groups": groups, 'friends': set(friends), 'unread_msg': unread_msg})


class SendMessageView(LoginRequiredMixin, View):
    """
    View with Sending Message to user
    """
    def get(self, request):
        form = SendMessageForm()
        friends = MyUser.objects.none()
        group = RunningGroup.objects.filter(members=request.user)
        for i in group:
            friends = (friends | i.members.all())
        form.fields['to'].queryset = friends.distinct('username').exclude(username=request.user.username)
        return render(request, 'racemate/form_html.html', {'form': form})

    def post(self, request):
        subject = request.POST.get("subject")
        content = request.POST.get('content')
        to = request.POST.get('to')

        sender = request.user
        if to:
            Message.objects.create(subject=subject, content=content,
                                   to=MyUser.objects.get(id=to), sender=sender)
            return redirect('messanger', id=to)

        return redirect('landing-page')


class SendMessageGroupView(LoginRequiredMixin, View):
    """
    View with Sending Message to group
    """
    def get(self, request):
        form = SendMessageGroupForm()
        form.fields['togroup'].queryset = RunningGroup.objects.all().filter(members=request.user)
        return render(request, 'racemate/form_html.html', {'form': form})

    def post(self, request):
        subject = request.POST.get("subject")
        content = request.POST.get('content')
        togroup = request.POST.get('togroup')
        sender = request.user
        if togroup:
            Message.objects.create(subject=subject, content=content,
                                   togroup=RunningGroup.objects.get(id=togroup), sender=sender)
            return redirect('forum', id=togroup)
        return redirect('landing-page')


class MessangerView(LoginRequiredMixin, View):
    """
    View with messages with one friend, and list with
    """
    def get(self, request, id):
        msg1 = Message.objects.filter(to=id).filter(sender=request.user).order_by('-date_sent')
        msg2 = (Message.objects.filter(sender=id).filter(to=request.user).order_by('-date_sent'))
        group = RunningGroup.objects.get(id=11)
        user = MyUser.objects.filter(members=group).exclude(id=request.user.id)
        msg = msg1 | msg2
        interlocutor = MyUser.objects.get(id=id)
        friends = []
        group = RunningGroup.objects.filter(members=request.user)
        for i in group:
            friend = i.members.all()
            for j in friend:
                friends.append(j)

        #  changing all unread messages as Read
        msg3 = Message.objects.filter(to=request.user)
        for i in msg3:
            i.read = True
            i.save()

        return render(request, 'messanger/messanger.html',
                      {"msg": msg, 'user': user, 'friends': set(friends), 'interlocutor': interlocutor})


class MessangerAllView(LoginRequiredMixin, View):
    """
    Test view - not included in urls
    """
    def get(self, request):
        friends = []
        groups = RunningGroup.objects.filter(members=request.user)
        for i in groups:
            friend = i.members.all()
            for j in friend:
                friends.append(j)

        return render(request, 'messanger/messanger_all.html', {'friends': set(friends), 'groups': groups})
