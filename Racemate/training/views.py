import datetime
import json

import isodate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from racemate.forms import AddTreningForm
from racemate.models import PastTraining, Training
from racemate.table import generateVDOT, TABLES


class AddTrainingView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'training/add_training.html', )

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
        return render(request, 'training/add_training.html', {'text': text})


class DeleteTrainingView(LoginRequiredMixin, View):
    def get(self, request, id):
        PastTraining.objects.get(id=id).delete()

        return redirect('landing-page')


class PastTrainingDelete(DeleteView):
    model = PastTraining

    success_url = reverse_lazy('landing-page')


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
        return render(request, "training/showtrening.html",
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

        return render(request, "training/showtrening.html", {"tr": plan, "dict": dicts})

    #
    # def createtraning(type, time, efficiency):
    #     speed = round(1 / TABLES[efficiency - 30][type + 6] * 3600, 2)
    #     distance = round(time * speed / 60, 2)
    #     return None


class LoadTreningView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "training/load.html")

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
        return render(request, "training/planchoice.html")


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
        return render(request, "training/showtrening.html", {"tr": a, "dict": dicts})
