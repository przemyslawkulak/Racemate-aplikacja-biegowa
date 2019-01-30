import datetime
import json

import isodate as isodate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, CreateView

from racemate.forms import LoginForm, PastTrainingForm, SendMessageForm, AddTreningForm, CreateGroupForm

from racemate.models import MyUser, RunningGroup, Message, PastTraining, Training
from racemate.table import TABLES, generateVDOT


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "racemate/start.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'racemate/login.html')

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
            return render(request, 'racemate/login.html')
            # jeśli nie uda się zalogować wraca na formularz
        return render(request, 'racemate/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)  # wylogowanie
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        return render(request, 'racemate/register.html')

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        users = MyUser.objects.all()
        usernames = []
        for i in users:
            usernames.append(i.username)
        if username and email and password and confirmPassword and password == confirmPassword:
            if username in usernames:
                text = 'Podany user już istnieje'
                return render(request, 'racemate/register.html', {"text": text})
            else:
                MyUser.objects.create_user(username=username,
                                           email=email,
                                           efficiency=30,
                                           password=password,
                                           )
                return redirect('login')
        text = 'Żle powtórzone hasło'
        return render(request, 'racemate/register.html', {"text": text})


def customhandler404(request):
    response = render(request, 'racemate/404.html', )
    response.status_code = 404
    return response


def customhandler500(request):
    response = render(request, 'racemate/500.html', )
    response.status_code = 500
    return response


class LandingView(LoginRequiredMixin, View):
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
        paginator = Paginator(training, 10)
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


class RunningGroupView(LoginRequiredMixin, View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        user = MyUser.objects.filter(members=group).order_by('id')

        return render(request, 'racemate/running-group.html', {'user': user, "group": group})


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
        return render(request, 'racemate/member.html',
                      {'member': member, 'msg': msg, 'interlocutor': interlocutor, "training": training})


class ForumView(LoginRequiredMixin, View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        user = MyUser.objects.filter(runninggroup=group).exclude(id=request.user.id)
        print(user)
        messages = Message.objects.filter(to__isnull=True).order_by('-date_sent')
        return render(request, 'racemate/forum.html', {'messages': messages, 'group': group, "user": user})


class AddTrainingView(LoginRequiredMixin, View):
    def get(self, request):
        form = PastTrainingForm()
        # return render(request, 'racemate/form_html.html', {'form': form})
        return render(request, 'racemate/add_training.html', )

    def post(self, request):
        name = request.POST.get("name")
        hours = request.POST.get('hours')
        minutes = request.POST.get('minutes')
        seconds = request.POST.get('seconds')
        distance_total = request.POST.get('distance')
        time = request.POST.get('time')
        date = request.POST.get('date')
        time_total = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        if (name is not None and time_total != 0 and distance_total and
                time and date and request.user is not None):

            distance_total = int(float(distance_total) * 1000)

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
        text = 'Wprowadź wszystkie dane do formularza'
        return render(request, 'racemate/add_training.html', {'text': text})


class SendMessageView(LoginRequiredMixin, View):
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
        return redirect('messanger', id=to)


class LandingGeneratorView(LoginRequiredMixin, View):
    def get(self, request, id):
        tr = PastTraining.objects.get(id=id)
        if isinstance(generateVDOT(tr), int):
            request.user.efficiency = generateVDOT(tr)
            request.user.save()
            return redirect('landing-page')
        else:
            return redirect('landing-page')


# class CreateGroupView(LoginRequiredMixin, CreateView):
#     fields = ['name']
#     model = RunningGroup
#     success_url = reverse_lazy('landing-page')

class CreateGroupView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateGroupForm
        return render(request, 'racemate/runninggroup_form.html', {'form': form})

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
        
        return render(request, 'racemate/showgroups.html', {"group": group})


class DeleteTrainingView(LoginRequiredMixin, View):
    def get(self, request, id):
        PastTraining.objects.get(id=id).delete()

        return redirect('landing-page')


class PastTrainingDelete(DeleteView):
    model = PastTraining

    success_url = reverse_lazy('landing-page')


class MessangerView(LoginRequiredMixin, View):
    def get(self, request, id):
        msg1 = Message.objects.filter(to=id).filter(sender=request.user).order_by('-date_sent')
        msg2 = (Message.objects.filter(sender=id).filter(to=request.user).order_by('-date_sent'))
        msg2 = (Message.objects.filter(sender=id).filter(to=request.user).order_by('-date_sent'))
        group = RunningGroup.objects.get(id=2)
        user = MyUser.objects.filter(runninggroup=group).exclude(id=request.user.id)
        msg = msg1 | msg2
        interlocutor = MyUser.objects.get(id=id)

        return render(request, 'racemate/messanger.html', {"msg": msg, 'user': user, 'interlocutor': interlocutor})


class AddTreningView(LoginRequiredMixin, View):
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


class TreningPlanWhiteView(LoginRequiredMixin, View):
    def get(self, request):
        plan = []
        tr = Training.objects.filter(treningplan='white')
        now = datetime.datetime.now()
        dic = []
        dicts = []
        for j in range(0, 4):
            for i in tr:
                total_distance = 0
                total_time = 0
                date = now + datetime.timedelta(days=i.trainingday + (j * 7) - 1)
                efficiency = request.user.efficiency
                speed = ''
                if i.walk is not None:
                    total_distance += traningdata(efficiency, i.walk, 7)[1]
                    total_time += i.walk
                    speed += "Marsz=" + str(round(traningdata(efficiency, i.walk, 7)[0], 2)) + 'km/h '
                    dic.append(1)

                if i.easy is not None:
                    total_distance += traningdata(efficiency, i.easy, 8)[1]
                    total_time += i.easy
                    speed += "BS=" + str(round(traningdata(efficiency, i.easy, 8)[0], 2)) + 'km/h '
                    dic.append(2)

                if i.marathon is not None:
                    total_distance += traningdata(efficiency, i.marathon, 9)[1]
                    total_time += i.marathon
                    speed += "M=" + str(round(traningdata(efficiency, i.easy, 9)[0], 2)) + 'km/h '
                    dic.append(3)

                if i.threshold is not None:
                    total_distance += traningdata(efficiency, i.threshold, 10)[1]
                    total_time += i.threshold
                    speed += "P=" + str(round(traningdata(efficiency, i.easy, 10)[0], 2)) + 'km/h '
                    dic.append(4)

                if i.interval is not None:
                    total_distance += traningdata(efficiency, i.interval, 11)[1]
                    total_time += i.interval
                    speed += "I=" + str(round(traningdata(efficiency, i.easy, 11)[0], 2)) + 'km/h'
                    dic.append(5)

                if i.repetition is not None:
                    total_distance += traningdata(efficiency, i.repetition, 12)[1]
                    total_time += i.repetition
                    speed += "R=" + str(round(traningdata(efficiency, i.easy, 12)[0], 2)) + 'km/h '
                    dic.append(6)

                plan.append({"name": i.name, "trainingday": i.trainingday + (j * 7), "date": date,
                             "total_run": i.easy, "total_time": i.time_total,
                             "total_distance": round(total_distance, 2),
                             "speed": speed,
                             "speed2": round(traningdata(efficiency, i.easy, 8)[0], 2)})

        if 1 in dic:
            dicts.append({"run": "Marsz - szybki marsz"})
        if 2 in dic:
            dicts.append({"run": "BS - bieg spokojny, w tempie konwersacyjnym"})
        if 3 in dic:
            dicts.append({"run": "M - bieg w tempie maratońskim"})
        if 4 in dic:
            dicts.append({"run": "P - szybki bieg progowy, do utrzymania przez 20-30 min"})
        if 5 in dic:
            dicts.append({"run": "I - bieg interwałowy, do utrzymania przez 2-3 min"})
        if 6 in dic:
            dicts.append({"run": "R - rytmy, badzo szybki bieg interwałowy, do utrzymania przez 0,5-1,5 minuty"})

        paginator = Paginator(plan, 12)
        page = request.GET.get('page')
        a = paginator.get_page(page)

        return render(request, "racemate/showtrening.html", {"tr": plan, "dict": dicts})


#
# def createtraning(type, time, efficiency):
#     speed = round(1 / TABLES[efficiency - 30][type + 6] * 3600, 2)
#     distance = round(time * speed / 60, 2)
#     return None
class LoadTreningView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "racemate/load.html")

    def post(self, request):
        with open('training.txt') as json_data:
            d = json.load(json_data)

            dur = isodate.parse_duration(d['duration'])
            time = dur.total_seconds()
            print(time)
            PastTraining.objects.create(
                time_total=time,
                distance_total=d['distance'],
                date=d['start-time'],
                user=request.user)

        # return render(request, "racemate/load.html", {"d": d})
        return redirect('landing-page')


class PlanChoiceView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "racemate/planchoice.html")


class TreningPlan18weeksView(LoginRequiredMixin, View):
    def get(self, request):
        plan = []
        tr = Training.objects.filter(treningplan='18weeks').order_by("trainingday")
        now = datetime.datetime.now()
        dic = []
        dicts = []
        for i in tr:
            total_distance = 0
            total_time = 0
            date = now + datetime.timedelta(days=i.trainingday - 1)
            efficiency = request.user.efficiency
            speed = ''
            if i.walk is not None:
                total_distance += traningdata(efficiency, i.walk, 7)[1]

                speed += "Marsz=" + str(round(traningdata(efficiency, i.walk, 7)[0], 2)) + 'km/h  '
                dic.append(1)

            if i.easy is not None:
                total_distance += traningdata(efficiency, i.easy, 8)[1]
                total_time += i.easy
                speed += "BS=" + str(round(traningdata(efficiency, i.easy, 8)[0], 2)) + 'km/h  '
                dic.append(2)

            if i.marathon is not None:
                total_distance += traningdata(efficiency, i.marathon, 9)[1]
                total_time += i.marathon
                speed += "M=" + str(round(traningdata(efficiency, i.marathon, 9)[0], 2)) + 'km/h  '
                dic.append(3)

            if i.threshold is not None:
                total_distance += traningdata(efficiency, i.threshold, 10)[1]
                total_time += i.threshold
                speed += "P=" + str(round(traningdata(efficiency, i.threshold, 10)[0], 2)) + 'km/h  '
                dic.append(4)

            if i.interval is not None:
                total_distance += traningdata(efficiency, i.interval, 11)[1]
                total_time += i.interval
                speed += "I=" + str(round(traningdata(efficiency, i.interval, 11)[0], 2)) + 'km/h  '
                dic.append(5)

            if i.repetition is not None:
                total_distance += traningdata(efficiency, i.repetition, 12)[1]
                total_time += i.repetition
                speed += "R=" + str(round(traningdata(efficiency, i.repetition, 12)[0], 2)) + 'km/h  '
                dic.append(6)

            plan.append({"name": i.name, "trainingday": i.trainingday, "date": date,
                         "total_run": total_time, "total_time": i.time_total,
                         "total_distance": round(total_distance, 2),
                         "speed": speed})

        if 1 in dic:
            dicts.append({"run": "Marsz - szybki marsz"})
        if 2 in dic:
            dicts.append({"run": "BS - bieg spokojny, w tempie konwersacyjnym"})
        if 3 in dic:
            dicts.append({"run": "M - bieg w tempie maratońskim"})
        if 4 in dic:
            dicts.append({"run": "P - szybki bieg progowy, do utrzymania przez 20-30 min"})
        if 5 in dic:
            dicts.append({"run": "I - bieg interwałowy, do utrzymania przez 2-3 min"})
        if 6 in dic:
            dicts.append({"run": "R - rytmy, badzo szybki bieg interwałowy, do utrzymania przez 0,5-1,5 minuty"})

        print(plan)
        paginator = Paginator(plan, 12)
        page = request.GET.get('page')
        a = paginator.get_page(page)
        print(dicts)
        return render(request, "racemate/showtrening.html", {"tr": a, "dict": dicts})
