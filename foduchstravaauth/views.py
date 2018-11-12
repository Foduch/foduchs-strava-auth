from django.conf import settings
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user
from foduchstravaauth.models import FoduchsStravaToken
from django.http import JsonResponse, HttpResponse
import datetime
from wsgiref.util import FileWrapper


def home_page(request):

    authorization_base_url = 'https://www.strava.com/oauth/authorize'
    client_id = settings.CLIENT_ID
    redirect_uri = settings.STRAVA_REDIRECT
    strava_access_link = authorization_base_url + '?response_type=code&approval_prompt=' \
                                                  'force&client_id={0}&redirect_uri={1}'.format(client_id, redirect_uri)
    user = get_user(request)
    return render(request, 'base.html', {'link': strava_access_link, 'user': user})


def strava_finish_login(request):

    code = request.GET['code']
    user = authenticate(request, code=code)
    login(request, user, backend='foduchstravaauth.backend.FoduchsStravaBackend')

    return redirect('/', {'user': user})

def get_activities(request):
    activities = []
    user = get_user(request)
    token = FoduchsStravaToken.objects.get(user=user)
    headers = {'Authorization': 'Bearer {0}'.format(token.token)}
    response = requests.get(settings.STRAVA_API_URL+'athlete/activities?per_page=10&page=1', headers=headers).json()

    result = []
    file = open('activities.csv', 'w+')
    file.write('Name,Type,Date,Distance,ElapsedTime,MovingTime,AvgSpeed,MaxSpeed,Elevation,AvgHRM,MaxHRM\n')
    for activity in response:
        res = {}
        res['average_speed'] = round(activity['average_speed']*3.6, 2)
        res['max_speed'] = round(activity['max_speed']*3.6, 2)
        res['name'] = activity['name']
        res['moving_time'] = str(datetime.timedelta(seconds=activity['moving_time']))
        res['type'] = activity['type']
        res['start_date'] = activity['start_date']
        res['total_elevation_gain'] = activity['total_elevation_gain']
        res['elapsed_time'] = str(datetime.timedelta(seconds=activity['elapsed_time']))
        res['distance'] = round(activity['distance']/1000, 2)
        if (activity['has_heartrate']):
            res['average_heartrate'] = activity['average_heartrate']
            res['max_heartrate'] = activity['max_heartrate']
        else:
            res['average_heartrate'] = 0
            res['max_heartrate'] = 0

        result.append(res)
        file.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(res['name'], res['type'], res['start_date'],
              res['distance'], res['elapsed_time'], res['moving_time'], res['average_speed'], res['max_speed'],
              res['total_elevation_gain'], res['average_heartrate'], res['max_heartrate']))
    file.close()

    response = HttpResponse(FileWrapper(open('activities.csv', 'rb')), content_type='application/csv')
    response['Content-Disposition'] = 'inline; filename=' + 'activities.csv'
    return response
    #return JsonResponse(result, safe=False)
