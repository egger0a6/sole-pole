from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import BooleanField, DateTimeField

# Create your models here.

class Poll(models.Model):
  title = models.CharField(max_length=280)
  notes = models.TextField(max_length=500, blank=True)
  public = models.BooleanField(default=False)
  expired = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
      return reverse("polls_detail", kwargs={"poll_id": self.id})


class Option(models.Model):
  title = models.CharField(max_length=100)
  count = models.PositiveIntegerField(default=0)
  poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

  def __str__(self):
    return self.title