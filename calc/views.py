from django.shortcuts import render

# Create your views here.
from django.views import View

from racemate.models import PastTraining
from racemate.table import generateVDOT


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
        time_total = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        print(form_value['hours'])
        if time_total != 0 and distance_total:
            distance_total = int(float(distance_total) * 1000)
            tr = PastTraining.objects.none()
            tr.distance_total = distance_total
            tr.time_total = time_total
            if isinstance(generateVDOT(tr), int):
                efficiency = generateVDOT(tr)

                return render(request, 'calc/calc.html', {'efficiency': efficiency, 'form_value': form_value})
        text = 'Insert all data to the form'
        return render(request, 'calc/calc.html', {'text': text})
