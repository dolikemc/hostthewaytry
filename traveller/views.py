# import the logging library
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from traveller.forms import UserForm, TravellerForm
from traveller.models import Traveller, PlaceAccount

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def update_traveller(request: HttpRequest, place_id: int, user_id: int) -> HttpResponse:
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


def register_user(request: HttpRequest, place_id: int) -> HttpResponse:
    """create a new user and add him to the admin group of the place"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        logging.debug(request.POST)

        if form.is_valid():
            user: User = form.save(commit=False)
            user.save()
            travellers = Traveller.objects.filter(user=user)
            for traveller in travellers:
                PlaceAccount.objects.create(place_id=place_id, traveller_id=traveller.id)
            messages.success(request, 'Account created successfully')
            return redirect('places:create-user', place_id=place_id, user_id=user.id)
    else:
        form = UserCreationForm()
    return render(request, 'traveller/register.html', {'form': form})


def register_worker(request: HttpRequest, ) -> HttpResponse:
    """create a new user and add him to the admin group of the place"""
    if request.method == 'POST':
        logging.debug(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user: User = form.save(commit=False)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('places:create-user', place_id=0, user_id=user.id)
    else:
        form = UserCreationForm()

    return render(request, 'traveller/register.html', {'form': form})
