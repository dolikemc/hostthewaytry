# import the logging library
import logging

# django moduls
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.forms import ModelForm, modelformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

# my models
from .models import Place, Price, Room

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'places/index.html'
    context_object_name = 'places'

    def get_queryset(self):
        # todo: measure of distance
        return Place.objects.order_by('-latitude')


# todo: load prices and room information to be displayed in the form
class DetailView(generic.DetailView):
    template_name = 'places/detail.html'
    context_object_name = 'place'
    model = Place


def base_layout(request: HttpRequest) -> HttpResponse:
    """ method to store base layout via service worker"""
    template = 'places/w3base.html'
    return render(request, template)


class NewPlaceMinimal(ModelForm):
    """form for the minimum of information creating a new place"""
    required_css_class = 'w3-light-blue'

    class Meta:
        model = Place
        fields = ['name', 'picture', 'description', 'laundry', 'parking',
                  'wifi', 'own_key', 'separate_entrance', 'who_lives_here']
        # user = User()


class AddUser(ModelForm):
    """add an administrator to a place"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


@login_required
def add_administrator_to_place(request: HttpRequest, place_id: int) -> HttpResponse:
    """create a new user and add him to the admin group of the place"""
    if request.method == 'POST':
        logging.debug(request.POST)
        form = AddUser(request.POST, request.FILES)
    else:
        form = AddUser()

    if form.is_valid():
        user = form.save(commit=False)
        place: Place = Place.objects.get(id=place_id)

        # todo: add permissions
        user.save()
        user.groups.add(place.group)
        user.save()
        return redirect('places:detail', pk=place_id)
    logger.warning(form.errors)
    return render(request, 'places/create_detail.html', {'form': form})


class EditPlace(ModelForm):
    """edit and create standard class for a place"""

    class Meta:
        model = Place
        exclude = ['longitude', 'latitude']
        # user = User(is_staff=True)


@login_required
def create_new_place(request: HttpRequest) -> HttpResponse:
    """cover the create new place process.
        first create a new user group
        than add the current user id to the group
        at last create a place just with the name, a picture and the user group id"""

    # todo: make access to request.user safe
    user = User.objects.get(pk=request.user.id)
    logger.debug(user)
    if request.method == 'POST':
        logger.debug(request.POST)

        group_name = request.POST.get('name', 'auto')
        index = 0
        while Group.objects.filter(name=group_name).count() > 0:
            group_name = group_name + str(index)
            index += 1
        group = Group.objects.create(name=group_name)
        user.groups.add(group)
        form = NewPlaceMinimal(request.POST, request.FILES)
    else:
        group = Group()
        form = NewPlaceMinimal()
    if form.is_valid():
        place = form.save(commit=False)
        place.group_id = group.id
        group.save()
        user.save()
        place.save()
        return redirect('places:detail', pk=place.pk)
    logger.warning(form.errors)
    return render(request, 'places/create_place.html', {'form': form})


@login_required
def create_new_place_v1(request: HttpRequest) -> HttpResponse:
    """create a new place old version"""
    if request.method == 'POST':
        logger.debug(request.POST)
        logger.debug(str(request.FILES))
        form = EditPlace(request.POST, request.FILES)
    else:
        form = EditPlace()
    if form.is_valid():
        place = form.save(commit=False)
        # make a few up shifts
        place.country = str.upper(place.country)
        place.languages = str.upper(place.languages)
        place.save()
        return redirect('places:detail', pk=place.pk)
    logger.warning(form.errors)
    return render(request, 'places/create_place.html', {'form': form})


# todo: use Styling required or erroneous form rows Form.error_css_class Form.required_css_class

class AddPriceToPlace(ModelForm):
    """add a price entry to the given place, therefore the place refernce is excluded"""
    required_css_class = 'w3-amber w3-input'

    class Meta:
        model = Price
        exclude = ['place']


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


class AddRoomToPlace(ModelForm):
    class Meta:
        model = Room
        exclude = ['place']
        localized_fields = ['valid_from', 'valid_to']


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


@login_required
def update_place(request: HttpRequest, pk: int) -> HttpResponse:
    room_form_set = modelformset_factory(model=Room, fields='__all__', max_num=1)
    price_form_set = modelformset_factory(model=Price, fields='__all__', max_num=3)
    place_form_set = modelformset_factory(model=Place, fields='__all__', max_num=1)
    logger.debug(request.POST)
    if request.method == 'POST':
        room_form_set = room_form_set(request.POST, request.FILES,
                                      queryset=Room.objects.filter(place_id__exact=pk),
                                      prefix='room')
        price_form_set = price_form_set(request.POST, request.FILES,
                                        queryset=Price.objects.filter(place_id__exact=pk),
                                        prefix='price')
        place_form_set = place_form_set(request.POST, request.FILES, queryset=Place.objects.filter(id=pk), )
        if room_form_set.is_valid() and price_form_set.is_valid() and place_form_set.is_valid():
            # todo: do something with the cleaned_data on the formsets.

            room_form_set.save()
            place_form_set.save()
            price_form_set.save()
            return redirect('places:detail', pk=pk)
        logger.debug(room_form_set.errors)
        logger.warning(price_form_set.errors)
        logger.warning(place_form_set.errors)
    else:
        room_form_set = room_form_set(prefix='room', queryset=Room.objects.filter(place_id__exact=pk), )
        price_form_set = price_form_set(prefix='price', queryset=Price.objects.filter(place_id__exact=pk), )
        place_form_set = place_form_set(queryset=Place.objects.filter(id=pk), )

    return render(request, 'places/create_place.html', {
        'formset': price_form_set,
        'room_formset': room_form_set,
        'form': place_form_set,
    })


def show_intro(request: HttpRequest) -> HttpResponse:
    """ just show the introduction, currently without database access"""
    return render(request, 'places/intro.html')
