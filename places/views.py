from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, inlineformset_factory, modelformset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from .models import Place, Price, Room


class IndexView(generic.ListView):
    template_name = 'places/index.html'
    context_object_name = 'places'

    def get_queryset(self):
        # todo: measure of distance
        return Place.objects.order_by('-latitude')


class DetailView(generic.DetailView):
    template_name = 'places/detail.html'
    context_object_name = 'place'
    model = Place


def base_layout(request: HttpRequest) -> HttpResponse:
    template = 'places/w3base.html'
    return render(request, template)


class CreatePlace(ModelForm):
    class Meta:
        model = Place
        # template_name = 'places/create_place.html'
        # todo: reduce fields and unit test still runs
        exclude = ['longitude', 'latitude']
        # fields = '__all__'
        # initial = {'name': 'Name', 'country': 'DE'}
        # user = User(is_staff=True)
        # localized_fields =

    # todo: split fields into optional and mandatory, eventually two screens (create and update)


@login_required
def create_new_place(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        print(request.POST, request.FILES)
        form = CreatePlace(request.POST, request.FILES)
    else:
        form = CreatePlace()
    if form.is_valid():
        place = form.save()
        return redirect('places:detail', pk=place.pk)
    return render(request, 'places/create_place.html', {'form': form})


@login_required
def change_place(request: HttpRequest, pk: int) -> HttpResponse:
    place = Place.objects.get(pk=pk)
    PlaceInlineFormset = inlineformset_factory(Place, Room, fields='__all__')
    if request.method == "POST":
        formset = PlaceInlineFormset(request.POST, request.FILES, instance=place)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect('places:detail', pk=place.pk)
    else:
        formset = PlaceInlineFormset(instance=place)
    return render(request, 'places/create_place.html', {'formset': formset})


# todo: use Styling required or erroneous form rows Form.error_css_class Form.required_css_class

class AddPriceToPlace(ModelForm):
    required_css_class = 'w3-amber'

    class Meta:
        model = Price
        fields = '__all__'


@login_required
def create_new_price(request: HttpRequest, place: int) -> HttpResponse:
    if request.method == 'POST':
        form = AddPriceToPlace(request.POST, request.FILES)
    else:
        form = AddPriceToPlace()
    if form.is_valid():
        price = form.save()
        return redirect('places:detail', pk=price.place_id)
    return render(request, 'places/create_price.html', {'form': form})


class AddRoomToPlace(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        localized_fields = ['valid_from', 'valid_to']


@login_required
def create_new_room(request: HttpRequest, place: int) -> HttpResponse:
    if request.method == 'POST':
        form = AddRoomToPlace(request.POST, request.FILES)
    else:
        form = AddRoomToPlace()
        form.place_id = place
    if form.is_valid():
        room = form.save()
        return redirect('places:detail', pk=room.place_id)
    return render(request, 'places/create_room.html', {'form': form})


@login_required
def update_place(request: HttpRequest, pk: int) -> HttpResponse:
    RoomFormSet = modelformset_factory(model=Room, fields='__all__', max_num=1)
    PriceFormSet = modelformset_factory(model=Price, fields='__all__', max_num=3)
    PlaceFormSet = modelformset_factory(model=Place, fields='__all__', max_num=1)
    if request.method == 'POST':
        room_form_set = RoomFormSet(request.POST, request.FILES,
                                    queryset=Room.objects.filter(place_id__exact=pk),
                                    prefix='room')
        price_form_set = PriceFormSet(request.POST, request.FILES,
                                      queryset=Price.objects.filter(place_id__exact=pk),
                                      prefix='price')
        place_form_set = PlaceFormSet(request.POST, request.FILES, queryset=Place.objects.filter(id=pk), )
        if room_form_set.is_valid() and price_form_set.is_valid() and place_form_set.is_valid():
            # do something with the cleaned_data on the formsets.
            room_form_set.save()
            place = place_form_set.save()
            price_form_set.save()
            return redirect('places:detail', pk=pk)
    else:
        room_form_set = RoomFormSet(prefix='room', queryset=Room.objects.filter(place_id__exact=pk), )
        price_form_set = PriceFormSet(prefix='price', queryset=Price.objects.filter(place_id__exact=pk), )
        place_form_set = PlaceFormSet(queryset=Place.objects.filter(id=pk), )
    return render(request, 'places/create_place.html', {
        'formset': price_form_set,
        'room_formset': room_form_set,
        'form': place_form_set,
    })
