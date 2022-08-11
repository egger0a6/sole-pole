from django.forms import ModelForm
from .models import Option

class OptionForm(ModelForm):
  class Meta:
    model = Option
    fields = ['title']