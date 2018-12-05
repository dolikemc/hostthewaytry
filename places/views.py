# import the logging library
import logging
from decimal import Decimal

# django modules
from django.contrib.auth.decorators import login_required, permission_required
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect

from places.forms import NewPlaceMinimal
# my models
from places.models import Place
from traveller.models import PlaceAccount, User

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


def base_layout(request: HttpRequest) -> HttpResponse:
    """ method to store base layout via service worker"""
    template = 'base.html'
    return render(request, template)


@atomic
@permission_required('places.add_place')
@login_required(login_url='/traveller/login/')
def create_new_place(request: HttpRequest) -> HttpResponse:
    """cover the create new place process."""
    if hasattr(request, 'user'):
        user: User = request.user
        logger.debug(request.user)
    else:
        return HttpResponseServerError()
    if request.method == 'POST':
        logger.debug(request.POST)
        form = NewPlaceMinimal(request.POST, request.FILES)
    else:
        form = NewPlaceMinimal()
    if form.is_valid():
        place: Place = form.save(commit=False)
        place.save()
        PlaceAccount.objects.create(place_id=place.id, user_id=user.id)
        # noinspection PyTypeChecker,PyCallByClass
        place.add_std_rooms_and_prices(std_price=Decimal(request.POST.get('std_price', '0.0')))
        return redirect('places:detail', pk=place.pk)
    logger.warning(form.errors)
    return render(request, 'places/create_place_minimal.html', {'form': form})


def show_intro(request: HttpRequest) -> HttpResponse:
    """ just show the introduction, currently without database access"""
    return render(request, 'places/intro.html')
