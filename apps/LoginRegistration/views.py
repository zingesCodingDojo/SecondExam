from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User


def index(request):
    """
    Main page will require the user to login (existing account) or create a new account (new user).
    :param request:
    :return:
    """
    if "logged_user" in request.session:
        return redirect(reverse("appointments:index"))

    return render(request, "LoginRegistration/index.html")


def register(request):
    """
    Registration form routing view. Contacts models for valid user registration formatting.
    :param request:
    :return:
    """
    if request.method == "POST":
        response_from_models = User.objects.registration_validaiton(request.POST)

        if response_from_models["status"]:
            new_user = response_from_models["new_user"]
            print(new_user.name)
        else:
            for errors in response_from_models["errors"]:
                messages.error(request, errors)
                # This will redirect

    return redirect("/")


def login(request):
    if request.method == "POST":
        response_from_models = User.objects.login_validation(request.POST)

        if response_from_models["status"]:
            print("I found the user and password matched.")
            request.session["logged_user"] = response_from_models["user"]
            request.session["full_user"] = response_from_models["full_user"]

        else:

            for errors in response_from_models["errors"]:
                print(errors)
                messages.error(request, errors)
            return redirect("/")

    return redirect(reverse("appointments:index"))
