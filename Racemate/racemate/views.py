from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from racemate.forms import UserForm, LoginForm
from racemate.models import MyUser, RunningGroup


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
        return render(request, "racemate/landing-page.html")


class RunningGroupView(View):
    def get(self, request, id):
        group = RunningGroup.objects.get(id=id)
        user = MyUser.objects.filter(runninggroup=group).order_by('id')

        return render(request, 'racemate/running-group.html', {'user': user, "group": group})


class MemberView(View):
    def get(self, request, id):
        member = MyUser.objects.get(id=id)
        return render(request, 'racemate/member.html', {'member': member})
