from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

# Модель события. 
class Event(models.Model):
    title = models.CharField(max_length=100, default='NULL')
    date = models.DateField(null=True, blank=True)
    text = models.TextField(default='', max_length=1000)
    user = models.ForeignKey(User, related_name='event_set', on_delete=models.CASCADE, null=True)
    participants = models.ManyToManyField(User, related_name='events_set')

    def __str__(self):
        return self.title