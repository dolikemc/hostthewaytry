# import the logging library
import logging
from decimal import Decimal

# django modules
from django.contrib.auth.decorators import login_required, permission_required
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import render, redirect

from places.forms import NewPlaceMinimal, AddRoomToPlace, AddPriceToPlace, EditPlaceView
# my models
from places.models import Place, Room
from traveller.models import PlaceAccount, User

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


def base_layout(request: HttpRequest) -> HttpResponse:
    """ method to store base layout via service worker"""
    template = 'base.html'
    return render(request, template)


@atomic
@login_required
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


@login_required
def create_new_price(request: HttpRequest, place: int) -> HttpResponse:
    """ new price added to a by id given place"""
    if request.method == 'POST':
        form = AddPriceToPlace(request.POST, request.FILES)
    else:
        form = AddPriceToPlace()
    logger.debug(request.POST)
    if form.is_valid():
        logger.debug(form.data)
        price = form.save(commit=False)
        price.place_id = place
        price.save()
        return redirect('places:detail', pk=price.place_id)
    logger.warning(form.errors)
    return render(request, 'places/create_detail.html', {'form': form})


@login_required
def create_new_room(request: HttpRequest, place: int) -> HttpResponse:
    if request.method == 'POST':
        form = AddRoomToPlace(request.POST, request.FILES)
    else:
        form = AddRoomToPlace()
        form.place_id = place
    logger.debug(request.POST)
    if form.is_valid():
        room: Room = form.save(commit=False)
        room.place_id = place
        room.save()

        return redirect('places:detail', pk=room.place_id)
    logger.warning(form.errors)
    return render(request, 'places/create_detail.html', {'form': form})


@permission_required('places.change_place')
@login_required
def update_place(request: HttpRequest, pk: int) -> HttpResponse:
    logger.debug(request.POST)
    place: Place = Place.objects.get(id=pk)
    if hasattr(request, 'user'):
        user: User = request.user
        logger.debug(user)
    else:
        return HttpResponseServerError()
    place_account: PlaceAccount = PlaceAccount.objects.filter(user_id=user.id, place_id=place.id).first()
    logger.debug(place_account)
    logger.debug(f"He's a SuperUser: {user.is_superuser}")
    if not user.is_superuser and place_account is None:
        logger.warning('no permission to change place')
        return HttpResponseForbidden()
    place.room_set.all()
    place.price_set.all()
    if request.method == 'POST':
        form = EditPlaceView(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            return redirect('places:detail', pk=pk)
        logger.warning(form.errors)
    else:
        form = EditPlaceView(instance=place)
        logger.debug(place)
        logger.debug(place.room_set.all())

    return render(request, 'places/create_place.html', {'form': form,
                                                        'rooms': place.room_set.all(),
                                                        'prices': place.price_set.all()})


def show_intro(request: HttpRequest) -> HttpResponse:
    """ just show the introduction, currently without database access"""
    return render(request, 'places/intro.html')
