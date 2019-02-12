import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from racemate.forms import CreateGroupForm
from racemate.models import RunningGroup, MyUser, Message, PastTraining


class RunningGroupView(LoginRequiredMixin, View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        user = MyUser.objects.filter(members=group).order_by('id')

        return render(request, 'group/running-group.html', {'user': user, "group": group})


class JoinGroupView(LoginRequiredMixin, View):
    def get(self, request):
        groups = []
        admin = []
        group = RunningGroup.objects.all().exclude(members=request.user)
        for i in group:
            admins = MyUser.objects.filter(admins=i)
            for j in admins:
                admin = j.username

            m = len(MyUser.objects.filter(members=i))
            groups.append({"name": i.name, "admins": admin, "members": m, "date": i.date, "id": i.id})
        return render(request, 'group/joingroup.html', {"groups": groups})


class JoinConfirmView(LoginRequiredMixin, View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        admins = MyUser.objects.filter(admins=group)
        for i in admins:
            Message.objects.create(content=f"Prośba o przyjęcie do grupy '{group.name}' ", sender=request.user, to=i,
                                   groupjoin=group)
        return redirect('running-group', id=id)


class AdminConfirmView(LoginRequiredMixin, View):
    def get(self, request, id, sender):
        g = RunningGroup.objects.get(id=id)
        m = MyUser.objects.get(id=sender)
        g.members.add(m)
        return redirect('running-group', id=id)


class MemberView(LoginRequiredMixin, View):
    def get(self, request, id):
        member = MyUser.objects.get(id=id)
        msg1 = Message.objects.filter(to=id).filter(sender=request.user).order_by('-date_sent')
        msg2 = (Message.objects.filter(sender=id).filter(to=request.user).order_by('-date_sent'))
        msg = msg1 | msg2
        interlocutor = MyUser.objects.get(id=id)
        training = []
        tra = PastTraining.objects.filter(user=id).order_by("-date")[:5]
        for i in tra:
            speed = round((float(i.distance_total) / float(i.time_total) * 3.6), 2)
            distance = i.distance_total / 1000
            training.append(
                {"speed": speed, 'time_total': str(datetime.timedelta(seconds=i.time_total)),
                 'distance_total': distance, 'user': i.user,
                 'date': i.date, "id": i.id})
        return render(request, 'group/member.html',
                      {'member': member, 'msg': msg, 'interlocutor': interlocutor, "training": training})


class CreateGroupView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateGroupForm
        return render(request, 'group/runninggroup_form.html', {'form': form})

    def post(self, request):
        form = CreateGroupForm(request.POST)
        user = request.user
        print(user)
        if form.is_valid():
            g = RunningGroup.objects.create(name=form['name'].value())
            g.admins.add(user)
            g.members.add(user)
        return redirect('show-groups')


class ShowGroupsView(View):
    def get(self, request):
        group = RunningGroup.objects.all().filter(members=request.user)
        return render(request, 'group/showgroups.html', {"group": group})

