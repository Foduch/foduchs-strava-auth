from django.urls import path
from .views import *


urlpatterns = [
    path('', strava_login, name='strava-login'),
    path('finishlogin/', strava_finish_login, name='strava-finish-login'),
]