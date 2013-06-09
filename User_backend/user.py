import sys
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from User_backend.models import User_preferences

from Tools.constants import *

User = get_user_model()
log = logging.getLogger(__name__)

def get_user_object(user):
    if isinstance(user, str) or isinstance(user, unicode):
        try:
            return User.objects.get(email = user)
        except User.DoesNotExist:
            return None
    elif isinstance(user, User):
        return user
    else:
        return None
    
def login_user(request):
    user = authenticate(email = request.POST['email'], \
                        password = request.POST['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            log.info("LogIN -- email = " + user.email + \
                     " | id = " + str(user.id))
            return USER_LOGGED_IN
        else:
            return USER_ACCOUNT_DISABLED
    else:
        return USER_INVALID

def logout_user(request):
    log.info("LogOUT - email = " + request.user.email + \
             " | id = " + str(request.user.id))
    logout(request)

def register_user(email, password, first_name, last_name):
    try:    # Remove this try and validate via js on the clientside itself
        user = User.objects.create_user(email, password)
    except IntegrityError:
        return False
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return True
    
def does_email_exist(email):
    return User.objects.filter(email = email).exists()

def get_first_name(user):
    return user.get_short_name()

def get_time_format(user):
    return 0
