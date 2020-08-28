from django.db import models
from django.utils import timezone


# Create your models here.


class Ticket(models.Model):
    title = models.CharField(max_length=50)
    post_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user_filed = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='New')
    user_assigned = models.CharField(max_length=50, blank=True, null=True)
    user_completed = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'
