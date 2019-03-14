from racemate.models import Message


def logged_user(request):
    ctx = {
        "user": request.user
    }
    if request.user.is_authenticated:
        ctx["auth"] = True
    else:
        ctx["auth"] = False
    return ctx


def unread_messages(request):
    if request.user.is_authenticated:
        number = Message.objects.filter(to=request.user).filter(read=False).count()
    else:
        number = 0
    ctx = {
        'unread_messages': number
    }
    return ctx


def join_to_group(request):
    if request.user.is_authenticated:
        number = Message.objects.filter(to=request.user).exclude(groupjoin=None).count()
    else:
        number = 0
    ctx = {
        'join_to_group': number
    }
    return ctx
