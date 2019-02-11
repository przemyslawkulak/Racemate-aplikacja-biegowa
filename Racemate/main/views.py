import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.

from django.views import View

from main.forms import LoginForm

from main.models import MyUser
from messanger.models import Message
from training.models import PastTraining


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "main/start.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'main/login.html')

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
            return render(request, 'main/login.html')
            # jeśli nie uda się zalogować wraca na formularz
        return render(request, 'main/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)  # wylogowanie
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        return render(request, 'main/register.html')

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
                return render(request, 'main/register.html', {"text": text})
            else:
                MyUser.objects.create_user(username=username,
                                           email=email,
                                           efficiency=30,
                                           password=password,
                                           )
                return redirect('login')
        text = 'Żle powtórzone hasło'
        return render(request, 'main/register.html', {"text": text})


def customhandler404(request):
    response = render(request, 'main/404.html', )
    response.status_code = 404
    return response


def customhandler500(request):
    response = render(request, 'main/500.html', )
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
        return render(request, "main/landing-page.html", {"training": a, "msg": m})
