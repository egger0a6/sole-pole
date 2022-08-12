import requests
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Poll, Option
from .forms import OptionForm, PollDateTimeForm
from django.utils import timezone

# Create your views here.

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def polls_index(request):
  all_polls = Poll.objects.all()
  for poll in all_polls:
    if poll.expires:
      if (poll.expires < timezone.now()):
        poll.expired = True
        poll.save()
  public_polls = Poll.objects.filter(public=True).filter(expired=False).order_by('expired')
  expired_polls = Poll.objects.filter(expired=True).order_by('expired')
  user_polls = []
  if(request.user.id):
    user_polls = Poll.objects.filter(user=request.user).order_by('expired')
  return render(request, 'polls/index.html', {
    'public_polls': public_polls,
    'user_polls': user_polls,
    'expired_polls': expired_polls
  })

def polls_detail(request, poll_id):
  poll = Poll.objects.get(id=poll_id)
  if poll.expires:
    if (poll.expires < timezone.now()):
      poll.expired = True
      poll.save()
  option_form = OptionForm()
  return render(request, 'polls/detail.html', {
    'poll': poll,
    'option_form': option_form,
  })

@login_required
def add_option(request, poll_id):
  form = OptionForm(request.POST)
  if form.is_valid():
    new_option = form.save(commit=False)
    new_option.poll_id = poll_id
    new_option.save()
  return redirect('polls_detail', poll_id=poll_id)

@login_required
def update_option(request, poll_id, option_id):
  option = Option.objects.get(id=option_id)
  option.count += 1
  option.save()
  return redirect('polls_detail', poll_id=poll_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('polls_index')
    else:
      error_message = 'Invalid sign-up => try again'
  
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)


class PollCreate(CreateView):
  form_class = PollDateTimeForm
  model = Poll

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)


class PollUpdate(LoginRequiredMixin, UpdateView):
  form_class = PollDateTimeForm
  model = Poll

class PollDelete(LoginRequiredMixin, DeleteView):
  model = Poll
  success_url = '/polls/'