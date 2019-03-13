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
from racemate.table import generateVDOT, adding_result


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "racemate/start.html")


class LoginView(View):
    def get(self, request):
        return render(request, 'racemate/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            users = [i.username for i in MyUser.objects.all()]
            if form['login'].value() in users:
                user = authenticate(username=form['login'].value(),
                                    password=form['password'].value())
                if user:
                    login(request, user)
                    return redirect('landing-page')
                text = 'Wrong password'
                return render(request, 'racemate/login.html', {'text': text})
            text = 'Unknown user'
            return render(request, 'racemate/login.html', {'text': text})
        text = 'Fill all fields'
        return render(request, 'racemate/login.html', {'text': text})


class LogoutView(View):
    def get(self, request):
        logout(request)
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
        usernames = [i.username for i in users]
        if username and email and password and confirmPassword:
            if password == confirmPassword:
                if username in usernames:
                    text = 'Username exists'
                    return render(request, 'racemate/register.html', {"text": text})
                else:
                    MyUser.objects.create_user(username=username,
                                               email=email,
                                               efficiency=30,
                                               password=password,
                                               )
                    return redirect('login')
            text = 'The password and confirmation password do not match'
            return render(request, 'racemate/register.html', {"text": text})

        text = 'Fill all fields'
        return render(request, 'racemate/register.html', {"text": text})


def customhandler404(request, exception=None):
    response = render(request, 'racemate/404.html', )
    response.status_code = 404
    return response


def customhandler500(request):
    response = render(request, 'racemate/500.html', )
    response.status_code = 500
    return response


class LandingView(LoginRequiredMixin, View):
    def get(self, request):

        # showing all trainings
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

        # last messages
        m = []
        msg = Message.objects.filter(to=request.user.id).order_by("-date_sent")
        for i in msg:
            m.append(
                {"subject": i.subject, 'content': i.content,
                 'to': i.to, 'user': request.user,
                 'sender': i.sender, "id": i.id})

        # showing personal records
        results = adding_result(request.user)
        print(results['half'])

        # showing groups where user is an admin
        groups = RunningGroup.objects.filter(admins=request.user.id)
        if training:
            last_training_day = training[0]['date'].date()
            now = datetime.date.today()
            days = (now-last_training_day).days
        else:
            days = 'no data'
        return render(request, "racemate/landing-page.html",
                      {"training": a, "msg": m, "groups": groups, 'results': results, 'days': days})


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
