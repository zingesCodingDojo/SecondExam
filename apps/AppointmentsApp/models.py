from __future__ import unicode_literals

from django.db import models
from ..LoginRegistration.models import User
from time import strftime
from django.utils import timezone


class AppointmentManager(models.Manager):
    def validation(self, postData, user_id):
        errors = []

        if len(postData["appointment_task"]) < 4:
            errors.append("Appointment Task cannot be less than 3 characters!")

        if len(postData["appointment_date"]) < 1:
            errors.append("Appointment date cannot be empty")

        elif len(postData["appointment_time"]) < 1:
            errors.append("Appointment time cannot be empty!")

        if postData["appointment_date"][:4] <= strftime("%Y") and postData["appointment_date"][5:7] <= strftime("%m") and \
                        postData["appointment_date"][8:10] <= strftime("%d"):
            errors.append("Your appointment cannot be from the past!")


        response_to_views = {}

        if len(errors):
            response_to_views["status"] = False
            response_to_views["errors"] = errors
        else:
            response_to_views["status"] = True
            new_appointment = self.create(user=User.objects.get(id=user_id), date=postData["appointment_date"],
                                          time=postData["appointment_time"], task=postData["appointment_task"],
                                          status="Pending")
            response_to_views["new_appointment"] = new_appointment

        return response_to_views

    def update(self, postData, appointment_id):
        errors = []
        now = timezone.now()
        if len(postData["appointment_task"]) < 4:
            errors.append("Appointment Task cannot be less than 3 characters!")

        if len(postData["appointment_date"]) < 1:
            errors.append("Appointment date cannot be empty")

        elif len(postData["appointment_time"]) < 1:
            errors.append("Appointment time cannot be empty!")

        elif int(postData["appointment_date"][:4]) < int(strftime("%Y")) and \
                        int(postData["appointment_date"][5:7]) < int(strftime("%m")) and \
                        int(postData["appointment_date"][8:10]) < int(strftime("%d")):
            errors.append("Date cannot be from the past!")

        elif postData["appointment_date"] < now:
            errors.append("Date cannot be from the past!")
        print(postData["appointment_date"])

        response_to_views = {}

        if len(errors):
            response_to_views["status"] = False
            response_to_views["errors"] = errors
        else:
            response_to_views["status"] = True
            get_appointment = self.get(id=appointment_id)


            response_to_views["new_appointment"] = get_appointment

        return response_to_views


class Appointment(models.Model):
    user = models.ForeignKey(User, related_name="user_appointment", on_delete=models.CASCADE)
    date = models.DateTimeField()
    time = models.CharField(max_length=20)
    task = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()
