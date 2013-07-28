from django.db import models
from people.models import Person

class OptIn(models.Model):
    attendee = models.ForeignKey(Person)
    date = models.DateField(auto_now_add=True)
    sug_location = models.CharField(max_length=50, null=True, blank=True)
    sug_time = models.TimeField(null=True, blank=True)





