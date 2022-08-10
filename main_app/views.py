import requests
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Poll
from .forms import OptionForm


# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def polls_index(request):
  polls = Poll.objects.all()
  return render(request, 'polls/index.html', {'polls': polls})

def polls_detail(request, poll_id):
  poll = Poll.objects.get(id=poll_id)
  option_form = OptionForm()
  return render(request, 'polls/detail.html', {
    'poll': poll,
    'option_form': option_form,
  })
