
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def authenticate_view(rqst):
    if rqst.method == 'POST':
        creds = json.loads(rqst.body.decode('utf-8'))
        username = creds['username']
        password = creds['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(rqst, user)
            return HttpResponse()
        return HttpResponse(status=403)
    return HttpResponse(status=404)

@login_required
def auth_check(rqst):
    if rqst.method == 'POST':
        resp = HttpResponse()
        resp.set_cookie('logged_in', 'true')
        return resp
    return HttpResponse(status=404)
