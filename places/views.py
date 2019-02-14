# import the logging library
import logging
from decimal import Decimal

# django modules
from django.contrib.auth.decorators import login_required, permission_required
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from places.forms import PlaceCategoryForm
# my models
from places.models import Place
from traveller.models import PlaceAccount

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


def base_layout(request: HttpRequest) -> HttpResponse:
    """ method to store base layout via service worker"""
    template = 'base.html'
    return render(request, template)


@atomic
@permission_required('places.delete_place')
@login_required(login_url='/traveller/login/')
def delete_place(request: HttpRequest, pk: int) -> HttpResponse:
    """set a place to deleted = true (soft delete)"""
    place = Place.objects.get(id=pk)
    if place is not None:
        place.deleted = True
        place.save()
    return redirect('places:detail', pk)


@atomic
@permission_required('places.change_place')
@login_required(login_url='/traveller/login/')
def undelete_place(request: HttpRequest, pk: int) -> HttpResponse:
    """set a place to deleted = true (soft delete)"""
    place = Place.objects.get(id=pk)
    if place is not None:
        place.deleted = False
        place.save()
    return redirect('places:detail', pk)


def show_intro(request: HttpRequest) -> HttpResponse:
    """ just show the introduction, currently without database access"""
    return render(request, 'places/intro.html')
