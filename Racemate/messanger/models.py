from django.db import models


# Create your models here.
from main.models import MyUser, RunningGroup


class Message(models.Model):
    subject = models.CharField(max_length=256, verbose_name="Temat")
    content = models.TextField(verbose_name="Treść wiadomości", null=True)
    to = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=True,
                           null=True, related_name="Adresat", verbose_name="Adresat")
    sender = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True,
                               related_name="Nadawca", verbose_name="Nadawca")
    date_sent = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Data wysłania")
    groupjoin = models.OneToOneField(RunningGroup, on_delete=models.CASCADE, null=True, related_name="Join")
    togroup = models.ForeignKey(RunningGroup, on_delete=models.CASCADE, blank=True, null=True,
                                related_name="Message", verbose_name="Wiadomość do grupy")
