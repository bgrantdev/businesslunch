from django.contrib.auth.models import User
from django.db import models
from django_localflavor_us.models import PhoneNumberField


class Person(models.Model):
    user = models.ForeignKey(User)
    phone = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name



