from django.conf import settings
import requests
from django.shortcuts import render
from django.contrib.auth import login, authenticate

def strava_login(request):
    authorization_base_url = 'https://www.strava.com/oauth/authorize'
    client_id = settings.CLIENT_ID
    redirect_uri = settings.STRAVA_REDIRECT

    strava_access_link = authorization_base_url + '?response_type=code&approval_prompt=force&client_id={0}&redirect_uri={1}'.format(
            client_id, redirect_uri)
    return render(request, 'base.html', {'link': strava_access_link})

def strava_finish_login(request):
    code = request.GET['code']

    user = authenticate(request, code=code)
    login(request, user, backend='foduchstravaauth.backend.MyBackend')

    return render(request, 'base.html', {'user': user})