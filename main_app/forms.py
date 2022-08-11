from django import forms
from django.forms import ModelForm
from .models import Option, Poll
from .widgets import DateTimePickerInput

class OptionForm(ModelForm):
  class Meta:
    model = Option
    fields = ['title']

class PollDateTimeForm(ModelForm):
  class Meta:
    model = Poll
    fields = ['title', 'notes', 'public', 'expires']
    widgets = {
      'expires': DateTimePickerInput
    }