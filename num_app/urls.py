from django.urls import path
from . import views


urlpatterns = [
    path('', views.start_game, name='start'),
    path('user_choice/', views.input_your_number, name='write_your_number'),
    ]