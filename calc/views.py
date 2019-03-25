from django.shortcuts import render

# Create your views here.
from django.views import View

from racemate.models import PastTraining
from racemate.table import generateVDOT, TABLES


class CalculatorView(View):
    def get(self, request):
        return render(request, 'calc/calc.html')

    def post(self, request):
        hours = request.POST.get('hours')
        minutes = request.POST.get('minutes')
        seconds = request.POST.get('seconds')
        distance_total = request.POST.get('distance')
        form_value = {}
        form_value["hours"] = hours
        form_value["minutes"] = minutes
        form_value["seconds"] = seconds
        form_value["distance_total"] = distance_total

        try:
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            distance_total = int(distance_total)

        except ValueError:
            text = 'Insert all data to the form'
            return render(request, 'calc/calc.html', {'text': text})

        if hours < 0 or minutes < 0 or seconds < 0 or distance_total < 0:
            text = 'No data can be a negative number'
            return render(request, 'calc/calc.html', {'text': text})

        if hours != 0 or minutes != 0 or seconds != 0:
            time_total = hours * 3600 + minutes * 60 + seconds
            if time_total != 0 and distance_total:
                distance_total = int(float(distance_total) * 1000)
                tr = PastTraining.objects.none()
                tr.distance_total = distance_total
                tr.time_total = time_total
                if isinstance(generateVDOT(tr), int):
                    efficiency = generateVDOT(tr)

                return render(request, 'calc/calc.html', {'efficiency': efficiency, 'form_value': form_value,
                                                          'results': adding_result(efficiency),
                                                          'tempos': adding_tempos(efficiency)})

        text = 'Insert all data to the form'
        return render(request, 'calc/calc.html', {'text': text})


def generate_result(efficiency, distance):
    if efficiency in range(30, 61) and isinstance(efficiency, int):
        if distance in range(1, 6) and isinstance(distance, int):
            total_time = TABLES[efficiency - 30][distance]
            hours = total_time // 3600
            minutes = (total_time - hours * 3600) // 60
            seconds = total_time - hours * 3600 - minutes * 60
            if hours > 0:
                hours = str(hours) + "h "
            else:
                hours = ''
            if minutes > 0:
                minutes = str(minutes) + "min "
            else:
                minutes = ''
            if seconds > 0:
                seconds = str(seconds) + "sec "
            else:
                seconds = ''

            return hours + minutes + seconds
        else:
            return "Incorrect distance"
    else:
        return "Incorrect efficiency"


def adding_result(efficiency):
    if efficiency in range(30, 61) and isinstance(efficiency, int):
        results = {}
        results['marathon'] = generate_result(efficiency, 5)
        results['half'] = generate_result(efficiency, 4)
        results['10k'] = generate_result(efficiency, 3)
        results['5k'] = generate_result(efficiency, 2)
        results['3k'] = generate_result(efficiency, 1)
        return results
    else:
        return 'Incorrect efficiency'


def generate_tempo(efficiency, type):
    if efficiency in range(30, 61) and isinstance(efficiency, int):
        if type in range(8, 13) and isinstance(type, int):
            return str(round(1 / TABLES[efficiency - 30][type] * 3600, 2)) + 'km/h'
        else:
            return 'Incorrect type'
    else:
        return 'Incorrect efficiency'


def adding_tempos(efficiency):
    if efficiency in range(30, 61) and isinstance(efficiency, int):
        tempo = {}
        tempo['easy'] = generate_tempo(efficiency, 8)
        tempo['marathon'] = generate_tempo(efficiency, 9)
        tempo['threshold'] = generate_tempo(efficiency, 10)
        tempo['interval'] = generate_tempo(efficiency, 11)
        tempo['repetition'] = generate_tempo(efficiency, 12)

        return tempo
    else:
        return 'Incorrect efficiency'
