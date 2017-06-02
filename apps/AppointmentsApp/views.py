from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from ..LoginRegistration.models import User
from .models import Appointment
from time import strftime
import datetime
from django.utils import timezone


def index(request):
    if "logged_user" in request.session:
        pass
    else:
        return redirect(reverse("loginregistration:index"))

    get_all = Appointment.objects.all()
    now = timezone.now()
    current_list = []
    new_list = []
    # Future items
    for items in get_all:
        if items.date >= now:
            current_list.append(items)


    # Current items
    for items in get_all:
        if items.date > now:
            new_list.append(items)

    context = {
        "appointments": current_list,
        "future": new_list

    }

    return render(request, "AppointmentsApp/index.html", context)


def logout(request):
    if request.method == "POST":
        del request.session["logged_user"]
    return redirect(reverse("loginregistration:index"))


def add(request):
    if request.method == "POST":
        print(request.POST)
        response_from_models = Appointment.objects.validation(request.POST, request.session["full_user"])

        if response_from_models["status"]:
            print(response_from_models["new_appointment"])

        else:
            for errors in response_from_models["errors"]:
                messages.error(request, errors)

    return redirect(reverse("loginregistration:index"))


def delete(request, id):
    Appointment.objects.get(id=id).delete()
    return redirect(reverse("appointments:index"))


def edit(request, id):
    if "logged_user" in request.session:
        pass
    else:
        return redirect(reverse("loginregistration:index"))
    context = {
        "current_appointment": Appointment.objects.get(id=id)
    }

    return render(request, "AppointmentsApp/update.html", context)


def update(request, id):
    if request.method == "POST":

        response_from_models = Appointment.objects.update(request.POST, id)

        if response_from_models["status"]:
            response_from_models["new_appointment"].task = request.POST["appointment_task"]
            response_from_models["new_appointment"].status = request.POST["appointment_status"]
            response_from_models["new_appointment"].time = request.POST["appointment_time"]
            response_from_models["new_appointment"].date = request.POST["appointment_date"]
            response_from_models["new_appointment"].save()

        else:
            for errors in response_from_models["errors"]:
                messages.error(request, errors)
                return render(request, "AppointmentsApp/update.html")

    return redirect("/")
