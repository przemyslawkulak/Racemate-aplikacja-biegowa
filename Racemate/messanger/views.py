from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from racemate.forms import SendMessageForm, SendMessageGroupForm
from racemate.models import RunningGroup, MyUser, Message


class ForumView(LoginRequiredMixin, View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        user = MyUser.objects.filter(members=group).exclude(id=request.user.id)
        print(user)
        messages = Message.objects.filter(togroup=group).order_by('-date_sent')
        return render(request, 'messanger/forum.html', {'messages': messages, 'group': group, "user": user})


class ForumChoiceView(LoginRequiredMixin, View):
    def get(self, request):
        groups = []
        admin = []
        group = RunningGroup.objects.all().filter(members=request.user)
        for i in group:
            admins = MyUser.objects.filter(admins=i)
            for j in admins:
                admin = j.username

            m = len(MyUser.objects.filter(members=i))
            groups.append({"name": i.name, "admins": admin, "members": m, "date": i.date, "id": i.id})
        return render(request, 'messanger/forumchoice.html', {"groups": groups})
    # def get(self, request):
    #     group = RunningGroup.objects.all().filter(members=request.user)
    #     return render(request, 'racemate/forumchoice.html', {'group': group})


class SendMessageView(LoginRequiredMixin, View):
    def get(self, request):
        form = SendMessageForm()
        form.fields['to'].queryset = MyUser.objects.all().exclude(id=request.user.id)
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
    def get(self, request, id):
        msg1 = Message.objects.filter(to=id).filter(sender=request.user).order_by('-date_sent')
        msg2 = (Message.objects.filter(sender=id).filter(to=request.user).order_by('-date_sent'))
        msg2 = (Message.objects.filter(sender=id).filter(to=request.user).order_by('-date_sent'))
        group = RunningGroup.objects.get(id=2)
        user = MyUser.objects.filter(members=group).exclude(id=request.user.id)
        msg = msg1 | msg2
        interlocutor = MyUser.objects.get(id=id)

        return render(request, 'messanger/messanger.html', {"msg": msg, 'user': user, 'interlocutor': interlocutor})
