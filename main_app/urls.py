from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('polls/', views.polls_index, name='polls_index'),
    path('polls/<int:poll_id>/', views.polls_detail, name='polls_detail'),
    path('polls/create', views.PollCreate.as_view(), name='polls_create'),
    path('polls/<int:pk>/update', views.PollUpdate.as_view(), name='polls_update'),
    path('polls/<int:pk>/delete', views.PollDelete.as_view(), name='polls_delete'),
    path('polls/<int:poll_id>/add_option/', views.add_option, name='add_option'),
    path('polls/<int:poll_id>/update_option/<int:option_id>/', views.update_option, name='update_option'),
    path('accounts/signup', views.signup, name='signup'),
]