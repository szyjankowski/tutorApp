from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect("profile")
    return render(request, "app/index.html")
