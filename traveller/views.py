# import the logging library
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from places.models import Place
from traveller.models import Traveller
from .forms import UserForm, TravellerForm

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def create_place_admin(request: HttpRequest, place_id: int, user_id: int) -> HttpResponse:
    user: User = User.objects.get(id=user_id)
    traveller: Traveller = Traveller.objects.get(id=user.traveller.id)

    if request.method == 'POST':
        logging.debug(request.POST)
        user_form = UserForm(request.POST, request.FILES, instance=user)
        traveller_form = TravellerForm(request.POST, request.FILES, instance=traveller)
        if user_form.is_valid() and traveller_form.is_valid():
            user_form.save(commit=True)
            traveller_form.save(commit=True)
            if place_id > 0:
                return redirect('places:detail', pk=place_id)
            return redirect('admin:index')
    else:
        user_form = UserForm(instance=user)
        traveller_form = TravellerForm(instance=traveller)

    logger.warning(user_form.errors)
    logger.warning(traveller_form.errors)
    return render(request, 'traveller/create_place_admin.html',
                  {'user_form': user_form,
                   'traveller_form': traveller_form})


def register(request: HttpRequest, place_id: int) -> HttpResponse:
    """create a new user and add him to the admin group of the place"""
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            user: User = f.save(commit=False)
            user.save()
            messages.success(request, 'Account created successfully')
            if place_id > 0:
                place: Place = Place.objects.get(id=place_id)
                user.groups.add(place.group)
                user.save()
                return redirect('places:create-user', place_id=place_id, user_id=user.id)
            # worker call change form

            return redirect('places:create-user', place_id=0, user_id=user.id)

    else:
        f = UserCreationForm()

    return render(request, 'traveller/register.html', {'form': f})
