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
from django.db.models import Sum


CHART_COLORS = [
  'ffcd00', 
  'ff3051', 
  '5eac24', 
  '1869b7',
  '6a4c93',
  '17c3b2',
  'e85d04',
  'ef476f',
  '80ed99',
  '073b4c',
  '00bbf9',
  '7678ed',
  '89b0ae',
  '840032',
  'ffdc5e'
]

def chart_url_builder(options):
  url_str = 'https://image-charts.com/chart?chbr=6&chco='
  chco = ''
  chd = ''
  chdl = ''
  chm = ''

  i = 0
  for option in options:
    chco += (CHART_COLORS[i] + ',')

    if (i == len(options) - 1):
      chd += str(option.count)
    else:
      chd += (str(option.count) + '|')
    
    chdl += option.title + '|'
    chm += f'N,000000,{i},,10|'

    i += 1

  url_str += chco
  url_str += '&chd=t:'
  url_str += chd
  url_str += '&chdl='
  url_str += chdl
  url_str += '&chdls=000000,15&chds=0,50000&chm='
  url_str += chm
  url_str += '&chma=0,0,10,10&chs=700x200&cht=bhg&chxs=0,000000,0,0,_&chxt=y&chan&chf=bg,s,EFEFEF11'

  return url_str


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
  options = Option.objects.filter(poll=poll_id)
  chart_url = ''
  
  if (options):
    chart_url = chart_url_builder(options)

  if poll.expires:
    if (poll.expires < timezone.now()):
      poll.expired = True
      poll.save()

  option_form = OptionForm()
  total_votes = Option.objects.filter(poll=poll_id).aggregate(Sum('count'))['count__sum']
  return render(request, 'polls/detail.html', {
    'poll': poll,
    'option_form': option_form,
    'total_votes': total_votes,
    'chart_url': chart_url,
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