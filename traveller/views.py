# import the logging library
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import *
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from traveller.forms import LoginForm, UserCreationForm
from traveller.models import User
from places.models import PlaceAccount

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


def register_user(request: HttpRequest, place_id: int = 0) -> HttpResponse:
    """create a new user and add him to the admin group of the place if place id is given"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        logging.debug(request.POST)
        if form.is_valid():
            user: User = form.save(commit=True)
            if place_id > 0:
                logger.debug(f'create place account for user {user} and place id {place_id}')
                PlaceAccount.objects.create(place_id=place_id, user_id=user.id)
                messages.success(request, 'Account created successfully')
                if request.user.is_worker:
                    logger.debug(f'add group place admin to user {user}')
                    user.groups.add(Group.objects.filter(name__iexact='PlaceAdmin').first())
                    return redirect('places:worker')
            return redirect('traveller:create-user', pk=user.id, place_id=place_id, )
    else:
        form = UserCreationForm()
    return render(request, 'traveller/register.html', {'form': form})


def login_user(request: HttpRequest) -> HttpResponse:
    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST['email']
        password = request.POST['password']
        # authenticate also failed if user is inactiv
        user = authenticate(username=username, password=password)
        logger.info(form.errors)
        if user is None:
            form.add_error(error=_('User could not be authenticated'), field=None)
            logger.info(form.errors)
            return render(request, 'traveller/login.html', {'form': form})
        login(request, user)
        if user.is_staff:
            return redirect('/admin/places/place/?deleted__exact=0&reviewed__exact=0')
        if user.is_worker and not user.is_place_admin:
            return redirect('places:worker')
        if user.is_place_admin:
            return redirect('places:place_admin')

        return redirect('places:index')  # anonymous or logged in traveller
    else:
        form = LoginForm()
    return render(request, 'traveller/login.html', {'form': form})
