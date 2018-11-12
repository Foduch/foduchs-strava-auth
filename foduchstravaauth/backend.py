from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
import requests
from .models import FoduchsStravaToken


class FoduchsStravaBackend:

    token_url = 'https://www.strava.com/api/v3/oauth/token'

    def authenticate(self, request, code):
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET




        response = requests.post(self.token_url, data={'client_id': client_id, 'client_secret': client_secret,
                                              'code': code}).json()
        access_token = response['access_token']
        user_id = response['athlete']['id']

        try:
            user = User.objects.get(pk = user_id)
        except:
            first_name = response['athlete']['firstname']
            last_name = response['athlete']['lastname']
            user_name = '{0} {1}'.format(first_name, last_name)
            user = User(id=user_id, username=user_name)
            user.save()

        (token, created) = FoduchsStravaToken.objects.get_or_create(user=user)
        token.token = access_token
        token.save()

        return user


    def get_user(self, user_id):

        try:
            return User.objects.get(id=user_id)
        except:
            return None
