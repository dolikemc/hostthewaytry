# import the logging library
import logging

# django modules
from django.contrib.auth.decorators import login_required, permission_required
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# my models
from places.models import Place

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


def set_deleted(deleted: bool, pk: int) -> HttpResponse:
    try:
        place = Place.objects.get(id=pk)
        place.deleted = deleted
        place.save()
        return redirect('places:detail', pk)
    except Place.DoesNotExist:
        return HttpResponse(status=404, content=f'place with id {pk} does not exist')


@atomic
@permission_required('places.delete_place')
@login_required(login_url='/traveller/login/')
def delete_place(request: HttpRequest, pk: int) -> HttpResponse:
    """set a place to deleted = true (soft delete)"""
    return set_deleted(True, pk)


@atomic
@permission_required('places.change_place')
@login_required(login_url='/traveller/login/')
def undelete_place(request: HttpRequest, pk: int) -> HttpResponse:
    """set a place to deleted = true (soft delete)"""
    return set_deleted(False, pk)


def show_intro(request: HttpRequest) -> HttpResponse:
    """ just show the introduction, currently without database access"""
    return render(request, 'places/intro.html')
