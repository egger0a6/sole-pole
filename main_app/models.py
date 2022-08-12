from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone, dateformat
from django.utils.timezone import now

# Create your models here.

class Poll(models.Model):
  formatted_date = dateformat.format(timezone.now(), 'Y-m-d H:i')

  title = models.CharField(max_length=280)
  notes = models.TextField(max_length=500, blank=True)
  public = models.BooleanField(default=True)
  expired = models.BooleanField(default=False)
  expires = models.DateTimeField(default=formatted_date, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title

  def clean(self, *args, **kwargs):
    super(Poll, self).clean(*args, **kwargs)
    if self.expires:
      if self.expires < timezone.now():
        raise ValidationError('Expiration time must be later than now.')

  def get_absolute_url(self):
      return reverse("polls_detail", kwargs={"poll_id": self.id})


class Option(models.Model):
  title = models.CharField(max_length=100)
  count = models.PositiveIntegerField(default=0)
  poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

  def __str__(self):
    return self.title