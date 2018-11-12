from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('logout', LogoutView.as_view(),{'next_page': ''}, name='logout'),
    path('strava/activities', get_activities, name='get-activities'),
    path('strava/finishlogin/', strava_finish_login, name='strava-finish-login'),
    path('', home_page, name='home-page'),

]