import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from racemate.forms import CreateGroupForm
from racemate.models import RunningGroup, MyUser, Message, PastTraining


class RunningGroupView(LoginRequiredMixin, View):
    """
    View with details of all members of the one running group
    """
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        user = MyUser.objects.filter(members=group).order_by('id')

        return render(request, 'group/running-group.html', {'user': user, "group": group})


class ShowGroupsView(LoginRequiredMixin, View):
    """
    View of all groups in which user is member, with details:
    - who is admin,
    - members count
    - date of creation
    """
    def get(self, request):
        groups = []
        admin = []
        group = RunningGroup.objects.all().filter(members=request.user)
        for i in group:
            admins = MyUser.objects.filter(admins=i)
            for j in admins:
                admin = j.username

            members_number = len(MyUser.objects.filter(members=i))
            groups.append({"name": i.name, "admins": admin, "members": members_number, "date": i.date, "id": i.id})
        return render(request, 'group/showgroups.html', {"groups": groups})


class JoinGroupView(LoginRequiredMixin, View):
    """
    View of all groups in which user is NOT member, with details:
    - who is admin,
    - members count
    - date of creation
    - if user sent a request to join
    """
    def get(self, request):
        groups = []
        admin = []
        group = RunningGroup.objects.all().exclude(members=request.user)
        join = Message.objects.filter(sender=request.user).exclude(groupjoin=None)
        group_join_id = {i.groupjoin.id for i in join}
        for i in group:
            admins = MyUser.objects.filter(admins=i)
            for j in admins:
                admin = j.username

            m = len(MyUser.objects.filter(members=i))
            groups.append({"name": i.name, "admins": admin, "members": m, "date": i.date, "id": i.id})
        return render(request, 'group/joingroup.html', {"groups": groups, 'join': group_join_id})


class JoinConfirmView(LoginRequiredMixin, View):
    """
    View to send a message to admin with request or showing text "you already request to group"
    """
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        admins = MyUser.objects.filter(admins=group)

        for i in admins:
            m = Message.objects.filter(groupjoin=group.id).filter(sender=request.user)
            if m:
                groups = []
                admin = []
                g = RunningGroup.objects.all().exclude(members=request.user)
                for i in g:
                    admins = MyUser.objects.filter(admins=i)
                    for j in admins:
                        admin = j.username
                    m = len(MyUser.objects.filter(members=i))
                    groups.append({"name": i.name, "admins": admin, "members": m, "date": i.date, "id": i.id})
                text = f'You already requested to {group.name}'
                return render(request, 'group/joingroup.html', {"groups": groups, "text": text})
            Message.objects.create(content=f"Request to join '{group.name}' ", sender=request.user, to=i,
                                   groupjoin=group)
        return redirect('running-group', id=id)


class AdminConfirmView(LoginRequiredMixin, View):
    """
    View to add another user to group
    """
    def get(self, request, id, sender):
        g = RunningGroup.objects.get(id=id)
        m = MyUser.objects.get(id=sender)
        g.members.add(m)
        Message.objects.filter(groupjoin=g).filter(sender=sender).delete()
        return redirect('running-group', id=id)


class MemberView(LoginRequiredMixin, View):
    """
    View to show detail of member of group
    - 5 last trainings
    - last messages with user
    """
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
    """
    View to insert name of group user'd like to create
    POST - creation of group
    """
    def get(self, request):
        form = CreateGroupForm
        return render(request, 'group/runninggroup_form.html', {'form': form})

    def post(self, request):
        form = CreateGroupForm(request.POST)
        user = request.user
        if form.is_valid():
            g = RunningGroup.objects.create(name=form['name'].value())
            g.admins.add(user)
            g.members.add(user)
        return redirect('show-groups')


class AdminView(LoginRequiredMixin, View):
    """
    View with users requested to join group which you are admin
    """
    def get(self, request, id):
        g = RunningGroup.objects.get(id=id)
        m = Message.objects.filter(groupjoin=g)
        requested_users = []
        for i in m:
            users = i.sender
            requested_users.append(
                {"id": users.id, "username": users.username, "email": users.email, "last_login": users.last_login})
        return render(request, 'group/admingroup.html', {"requested_users": requested_users, "group_id": id})


class ShowAdminView(LoginRequiredMixin, View):
    """
    View with list of group where user is admin
    """
    def get(self, request):
        join = Message.objects.filter(to=request.user).exclude(groupjoin=None)
        groups = RunningGroup.objects.filter(admins=request.user.id)
        return render(request, 'group/showadmin.html', {'groups': groups, 'join': join})
