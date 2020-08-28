from django.db import models
from django.utils import timezone

from bugtracker.settings import AUTH_USER_MODEL as newauthmodel


# Create your models here.


class Ticket(models.Model):
    title = models.CharField(max_length=50)
    post_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user_filed = models.ForeignKey(newauthmodel, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='New')
    user_assigned = models.CharField(max_length=50, blank=True, null=True)
    user_completed = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'
