import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from django.views import View
from django.views.generic import UpdateView

from racemate.forms import LoginForm, ContactForm

from racemate.models import MyUser, Message, PastTraining, RunningGroup
from racemate.table import generateVDOT


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
        groups = RunningGroup.objects.filter(admins=request.user.id)
        return render(request, "racemate/landing-page.html", {"training": a, "msg": m, "groups": groups})


class LandingGeneratorView(LoginRequiredMixin, View):
    def get(self, request, id):
        tr = PastTraining.objects.get(id=id)
        if isinstance(generateVDOT(tr), int):
            request.user.efficiency = generateVDOT(tr)
            request.user.save()
            return redirect('landing-page')
        else:
            return redirect('landing-page')


class EditUserView(LoginRequiredMixin, UpdateView):
    model = MyUser

    fields = ['username', 'first_name', 'last_name', 'email']
    template_name_suffix = '_update_form'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('edituser')


class ContactView(View):
    def get(self, request):
        form = ContactForm
        return render(request, 'racemate/contact.html', {"form": form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            email = form.cleaned_data['email']
            content = content + email
            send_mail(
                subject,
                content,
                'racemate.app@gmail.com',
                ['przemyslaw.kulak86@gmail.com'],
                fail_silently=False,
            )
            return redirect('landing-page')  # Todo  sending without getting emailin form
        return redirect('landing-page')


class AboutView(View):
    def get(self, request):
        return render(request, 'racemate/about.html', )
