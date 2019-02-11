from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from group.forms import CreateGroupForm
from group.models import RunningGroup
from main.models import MyUser
from messanger.models import Message


class RunningGroupView(LoginRequiredMixin, View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        user = MyUser.objects.filter(members=group).order_by('id')

        return render(request, 'main/running-group.html', {'user': user, "group": group})


class JoinGroupView(LoginRequiredMixin, View):
    def get(self, request):
        groups = []
        admin = []
        group = RunningGroup.objects.all().exclude(members=request.user)
        print(groups)
        for i in group:
            admins = MyUser.objects.filter(admins=i)
            for j in admins:
                admin = j.username

            m = len(MyUser.objects.filter(members=i))
            groups.append({"name": i.name, "admins": admin, "members": m, "date": i.date, "id": i.id})
        return render(request, 'main/joingroup.html', {"groups": groups})


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


class CreateGroupView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateGroupForm
        return render(request, 'main/runninggroup_form.html', {'form': form})

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
        return render(request, 'main/showgroups.html', {"group": group})
