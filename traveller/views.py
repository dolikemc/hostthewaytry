# import the logging library
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import redirect
from django.shortcuts import render

from traveller.forms import UserForm, LoginForm, UserCreationForm
from traveller.models import PlaceAccount, User

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def update_traveller(request: HttpRequest, place_id: int, user_id: int) -> HttpResponse:
    user: User = User.objects.get(id=user_id)

    if request.method == 'POST':
        logging.debug(request.POST)
        user_form = UserForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save(commit=True)
            # traveller_form.save(commit=True)
            if place_id > 0:
                return redirect('places:detail', pk=place_id)
            return redirect('admin:index')
    else:
        user_form = UserForm(instance=user)

    logger.warning(user_form.errors)
    return render(request, 'traveller/create_place_admin.html',
                  {'user_form': user_form, })


def register_user(request: HttpRequest, place_id: int) -> HttpResponse:
    """create a new user and add him to the admin group of the place"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        logging.debug(request.POST)

        if form.is_valid():
            user: User = form.save(commit=False)
            user.save()
            PlaceAccount.objects.create(place_id=place_id, user_id=user.id)
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


def login_user(request: HttpRequest, ) -> HttpResponse:
    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/places/')
    else:
        form = LoginForm()
    return render(request, 'traveller/login.html', {'form': form})
