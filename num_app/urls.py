from django.urls import path
from .views import StartGameView, InputYourNumberView


urlpatterns = [
    path('', StartGameView.as_view(), name='start'),
    path('user_choice/', InputYourNumberView.as_view(), name='write_your_number'),
    ]