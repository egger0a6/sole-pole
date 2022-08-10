from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('polls/', views.polls_index, name='polls_index'),
    path('polls/<int:poll_id>/', views.polls_detail, name='polls_detail'),
    path('polls/create', views.PollCreate.as_view(), name='polls_create'),
    path('accounts/signup', views.signup, name='signup'),
]
