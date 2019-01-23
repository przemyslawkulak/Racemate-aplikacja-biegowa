import datetime

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from racemate.forms import UserForm, LoginForm, PastTrainingForm, SendMessageForm, AddTreningForm
# PastTrainingForm
from racemate.models import MyUser, RunningGroup, Message, PastTraining, Training
from racemate.table import TABLES, generateVDOT


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
                 'date': i.date, "id": i.id})
        paginator = Paginator(training, 5)
        page = request.GET.get('page')
        a = paginator.get_page(page)
        m = []
        msg = Message.objects.filter(to=request.user.id).order_by("-date_sent")
        for i in msg:
            m.append(
                {"subject": i.subject, 'content': i.content,
                 'to': i.to, 'user': request.user,
                 'sender': i.sender, "id": i.id})
        return render(request, "racemate/landing-page.html", {"training": a, "msg": m})


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
        user = MyUser.objects.filter(runninggroup=group).exclude(id=request.user.id)
        print(user)
        messages = Message.objects.filter(to__isnull=True).order_by('-date_sent')
        return render(request, 'racemate/forum.html', {'messages': messages, 'group': group, "user": user})


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
        tr = PastTraining.objects.create(name=name,
                                         time_total=time_total,
                                         distance_total=distance_total,
                                         date=datetime,
                                         user=request.user)
        if ('VDOT' in request.POST) and isinstance(generateVDOT(tr), int):
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
        return redirect('forum/2')


class LandingGeneratorView(View):
    def get(self, request, id):
        tr = PastTraining.objects.get(id=id)
        if isinstance(generateVDOT(tr), int):
            request.user.efficiency = generateVDOT(tr)
            request.user.save()
            return redirect('landing-page')
        else:
            return redirect('landing-page')


class MessangerView(View):
    def get(self, request, id):
        msg1 = Message.objects.filter(to=id).filter(sender=request.user).order_by('-date_sent')
        msg2 = (Message.objects.filter(sender=id).filter(to=request.user).order_by('-date_sent'))
        group = RunningGroup.objects.get(id=2)
        user = MyUser.objects.filter(runninggroup=group).exclude(id=request.user.id)
        msg = msg1 | msg2

        return render(request, 'racemate/messanger.html', {"msg": msg, 'user': user})


class AddTreningView(View):
    def get(self, request):
        form = AddTreningForm
        return render(request, "racemate/form_html.html", {"form": form})

    def post(self, request):
        form = AddTreningForm(request.POST)
        rtype = int(form['type'].value())
        name = form['name'].value()
        timetrening = int(form['time'].value())
        efficiency = request.user.efficiency
        speed = round(1 / TABLES[efficiency - 30][rtype + 6] * 3600, 2)
        distance = round(timetrening * speed / 60, 2)
        return render(request, "racemate/showtrening.html",
                      {"type": rtype, "name": name, "time": timetrening,
                       "efficiency": efficiency, "speed": speed, "distance": distance})


def traningdata(efficiency, time, table):
    result = []
    speed = 1 / TABLES[efficiency - 30][table] * 3600
    distance = time * speed / 60
    result.append(speed)
    result.append(distance)
    return result


class TreningPlanView(View):
    def get(self, request):
        plan = []
        tr = Training.objects.all()
        now = datetime.datetime.now()

        for i in tr:
            total_distance = 0
            total_time = 0
            date = now + datetime.timedelta(days=i.trainingday - 1)
            efficiency = request.user.efficiency

            if i.walk is not None:
                total_distance += traningdata(efficiency, i.walk, 7)[1]
                total_time += i.walk

            if i.easy is not None:
                total_distance += traningdata(efficiency, i.easy, 8)[1]
                total_time += i.easy

            if i.marathon is not None:
                total_distance += traningdata(efficiency, i.marathon, 9)[1]
                total_time += i.marathon

            if i.threshold is not None:
                total_distance += traningdata(efficiency, i.threshold, 10)[1]
                total_time += i.threshold

            if i.interval is not None:
                total_distance += traningdata(efficiency, i.interval, 11)[1]
                total_time += i.interval

            if i.repetition is not None:
                total_distance += traningdata(efficiency, i.repetition, 12)[1]
                total_time += i.repetition

            plan.append({"name": i.name, "trainingday": i.trainingday, "date": date,
                         "total_run": i.easy, "total_time": total_time, "total_distance": round(total_distance, 2),
                         "speed1": round(traningdata(efficiency, i.walk, 7)[0], 2),
                         "speed2": round(traningdata(efficiency, i.easy, 8)[0], 2)})
            paginator = Paginator(plan, 2)
            page = request.GET.get('page')
            a = paginator.get_page(page)

        return render(request, "racemate/showtrening.html", {"tr": a})


def createtraning(type, time, efficiency):
    speed = round(1 / TABLES[efficiency - 30][type + 6] * 3600, 2)
    distance = round(time * speed / 60, 2)
    return None
