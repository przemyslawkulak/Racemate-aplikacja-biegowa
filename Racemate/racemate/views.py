import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from racemate.forms import UserForm, LoginForm, PastTrainingForm, SendMessageForm
# PastTrainingForm
from racemate.models import MyUser, RunningGroup, Message, PastTraining


class Index(View):
    def get(self, request):
        return render(request, "racemate/start.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'racemate/form_html.html', {'form': form})

    def post(self, request):
        '''

        :param request:
        :return:
        '''
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['login'].value(),
                                # wyciągamy login i hasło z formularza i logujemy
                                password=form['password'].value())
            if user:
                login(request, user)  # logujemy
                return redirect('landing-page')
                # jeśli uda się zalogować przerzuca nas na główną stronę
            return render(request, 'racemate/form_html.html', {'form': form})
            # jeśli nie uda się zalogować wraca na formularz
        return render(request, 'racemate/form_html.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)  # wylogowanie
        return redirect('login')


class LandingView(View):
    def get(self, request):
        training = []
        tra = PastTraining.objects.filter(user=request.user.id).order_by("-date")
        for i in tra:
            speed = round((float(i.distance_total) / float(i.time_total) * 3.6), 2)
            distance = i.distance_total / 1000
            training.append(
                {"speed": speed, 'time_total': str(datetime.timedelta(seconds=i.time_total)),
                 'distance_total': distance, 'user': i.user,
                 'date': i.date})
        return render(request, "racemate/landing-page.html", {"training": training, })


class RunningGroupView(View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        user = MyUser.objects.filter(runninggroup=group).order_by('id')

        return render(request, 'racemate/running-group.html', {'user': user, "group": group})


class MemberView(View):
    def get(self, request, id):
        member = MyUser.objects.get(id=id)
        return render(request, 'racemate/member.html', {'member': member})


class ForumView(View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        messages = Message.objects.filter(to__isnull=True).order_by('-date_sent')
        return render(request, 'racemate/forum.html', {'messages': messages, 'group': group})


class AddTrainingView(View):
    def get(self, request):
        form = PastTrainingForm()
        # return render(request, 'racemate/form_html.html', {'form': form})
        return render(request, 'racemate/add_training.html', )

    def post(self, request):
        name = request.POST.get("name")
        hours = request.POST.get('hours')
        minutes = request.POST.get('minutes')
        seconds = request.POST.get('seconds')
        time_total = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        distance_total = request.POST.get('distance')
        distance_total = int(float(distance_total) * 1000)
        time = request.POST.get('time')
        date = request.POST.get('date')
        datetime = date + ' ' + time
        PastTraining.objects.create(name=name, time_total=time_total, distance_total=distance_total, date=datetime,
                                    user=request.user)
        return redirect('landing-page')


class SendMessageView(View):
    def get(self, request):
        form = SendMessageForm
        return render(request, 'racemate/form_html.html', {'form': form})

    def post(self, request):
        form = SendMessageForm(request.POST)
        a = form['sender'].value()
        print(a)
        if form.is_valid():
            Message.objects.create(content=form['content'].value(), sender=request.user, to=form['to'].value())
        return render(request, "racemate/form_html.html", {"form": form})

    def post(self, request):
        subject = request.POST.get("subject")
        content = request.POST.get('content')
        to = request.POST.get('to')
        sender = request.user
        Message.objects.create(subject=subject, content=content, to=MyUser.objects.get(id=to), sender=sender)
        return redirect('landing-page')
