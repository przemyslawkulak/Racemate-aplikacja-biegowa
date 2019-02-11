def logged_user(request):
    ctx = {
        "user": request.user
    }
    if request.user.is_authenticated:
        ctx["auth"] = True
    else:
        ctx["auth"] = False
    return ctx
