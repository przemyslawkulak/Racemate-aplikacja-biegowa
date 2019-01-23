import datetime

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from racemate.forms import UserForm, LoginForm, PastTrainingForm, SendMessageForm
# PastTrainingForm
from racemate.models import MyUser, RunningGroup, Message, PastTraining
from racemate.table import TABLES


def checktable3(time):
    for i in range(0, 30):
        if time > TABLES[0][1]:
            vdot = 30
            return vdot
        elif time < TABLES[i][1] and time > TABLES[i + 1][1]:
            vdot = TABLES[i][0]
            return vdot
        else:
            vdot = 60
            return vdot


def generateVDOT(tr):
    if tr.distance_total < 3000:
        print('nie mierzone')
        return f'VDOT generujemy od dystansu 3 km'


    elif tr.distance_total > 3000 and tr.distance_total < 5000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(3000 / (speed / 3.6))
        print('3km')
        for i in range(0, 30):
            if time > TABLES[0][1]:
                vdot = 30
                return vdot
            elif time < TABLES[i][1] and time > TABLES[i + 1][1]:
                vdot = TABLES[i][0]
                return vdot
            elif time < TABLES[30][1]:
                vdot = 60
                return vdot


    elif tr.distance_total > 5000 and tr.distance_total < 10000:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(5000 / (speed / 3.6))
        print('5 km')
        for i in range(0, 30):
            if time > TABLES[0][2]:
                vdot = 30
                return vdot
            elif time < TABLES[i][2] and time > TABLES[i + 1][2]:
                vdot = TABLES[i][0]
                return vdot
            elif time < TABLES[30][2]:
                vdot = 60
                return vdot

    elif tr.distance_total > 10000 and tr.distance_total < 21097:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(10000 / (speed / 3.6))
        print('10 km')
        for i in range(0, 30):
            if time > TABLES[0][3]:
                vdot = 30
                return vdot
            elif time < TABLES[i][3] and time > TABLES[i + 1][3]:
                vdot = TABLES[i][0]
                return vdot
            elif time < TABLES[30][3]:
                vdot = 60
                return vdot


    elif tr.distance_total > 21097 and tr.distance_total < 42195:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(21097 / (speed / 3.6))
        print('Pół')
        for i in range(0, 30):
            if time > TABLES[0][4]:
                vdot = 30
                return vdot
            elif time < TABLES[i][4] and time > TABLES[i + 1][4]:
                vdot = TABLES[i][0]
                return vdot
            elif time < TABLES[30][4]:
                vdot = 60
                return vdot

    elif tr.distance_total > 42195:
        speed = round((float(tr.distance_total) / float(tr.time_total) * 3.6), 2)
        time = int(42195 / (speed / 3.6))
        print(tr.distance_total)
        print(tr.time_total)
        print(speed)
        print(time)
        print('Maraton')
        print(TABLES[0][5])
        for i in range(0, 30):
            if time > TABLES[0][5]:
                vdot = 30
                return vdot
            elif time < int(TABLES[i][5]) and time > int(TABLES[i + 1][5]):
                print(TABLES[i][5])
                vdot = TABLES[i][0]
                return vdot
            elif time < TABLES[30][5]:
                vdot = 60
                return vdot


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
        tr = PastTraining.objects.create(name=name, time_total=time_total, distance_total=distance_total, date=datetime,
                                         user=request.user)
        print(generateVDOT(tr))
        request.user.efficiency = generateVDOT(tr)
        request.user.save()
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
