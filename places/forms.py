# import the logging library
import logging

# django modules
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.db.transaction import atomic
from django.forms import ModelForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from django.views import generic

# my models
from places.models import Place, Price, Room, PlaceAccount, Categories
from traveller.models import User

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class DetailView(generic.DetailView):
    template_name = 'places/detail_edit.html'
    context_object_name = 'place'
    model = Place


class BaseIndexView(generic.ListView):
    """ Base class for index view on model place """
    model = Place
    context_object_name = 'places'

    def get_queryset(self):
        return Place.objects.filter(deleted__exact=False, placeaccount__user__exact=self.request.user
                                    ).order_by('-created_on')


class LoginRequiredWithURL(LoginRequiredMixin):
    login_url = '/traveller/login/'


class IndexPlaceAdminView(LoginRequiredWithURL, BaseIndexView):
    template_name = 'places/place_admin_index.html'


class IndexWorkerView(LoginRequiredWithURL, BaseIndexView):
    template_name = 'places/worker_index.html'


class IndexHistoryView(LoginRequiredWithURL, BaseIndexView):
    template_name = 'places/histories_index.html'


class IndexFilterView(LoginRequiredWithURL, BaseIndexView):
    template_name = 'places/filter_index.html'

    def get_queryset(self):
        # todo: measure of distance
        return Place.objects.filter(deleted__exact=False, reviewed__exact=True).order_by('-latitude')


class IndexView(BaseIndexView):
    template_name = 'places/index.html'

    def get_queryset(self):
        # todo: measure of distance
        return Place.objects.filter(deleted__exact=False, reviewed__exact=True).order_by('-latitude')


class BaseDeleteView(LoginRequiredWithURL, UserPassesTestMixin, PermissionRequiredMixin, generic.DeleteView):
    """ Base delete form, implements a common test function, the success url and skip confirmation"""
    permission_required = 'places.delete_place'

    def test_func(self):
        # the use of get_object() is necessary, because self.object not set yet
        return PlaceAccount.edit_place_permission(self.request.user, self.get_object().place.id)

    def get_success_url(self):
        return reverse('places:update-place', kwargs={'pk': self.object.place.id})

    def get(self, *args, **kwargs):  # skips confirmation
        return self.post(*args, **kwargs)


class DeletePrice(BaseDeleteView):
    model = Price


class DeleteRoom(BaseDeleteView):
    model = Room


class BaseChangeView(LoginRequiredWithURL, UserPassesTestMixin, PermissionRequiredMixin, generic.UpdateView):
    """Base change form, implements a common test function and the success url. If model is not a detail of
    the place model, but place itself, we can take the id direct from the self.get_object() return value
    and redirect after success to the detail page"""
    template_name = 'places/create_detail.html'
    context_object_name = 'form'
    permission_required = 'places.change_place'

    def test_func(self):
        # the use of get_object() is necessary, because self.object not set yet
        if self.model == Place:
            return PlaceAccount.edit_place_permission(self.request.user, self.get_object().id)
        return PlaceAccount.edit_place_permission(self.request.user, self.get_object().place.id)

    def get_success_url(self):
        if self.model == Place:
            return reverse('places:detail', kwargs={'pk': self.object.id})
        return reverse('places:update-place', kwargs={'pk': self.object.place.id})


class ChangePrice(BaseChangeView):
    model = Price
    fields = ['category', 'value', 'description']


class ChangeRoom(BaseChangeView):
    model = Room
    fields = ['room_number', 'beds', 'bathroom', 'kitchen', 'outdoor_place', 'room_add', 'smoking', 'pets', 'family',
              'handicapped_enabled', 'price_per_person', 'price_per_room', 'valid_from', 'valid_to']


class ChangePlaceAddress(BaseChangeView):
    model = Place
    fields = ['name', 'street', 'country', 'city', 'address_add', 'mobile', 'phone']

    def form_valid(self, form):
        logger.debug(self.request.POST)
        place = form.save(commit=False)
        place.country = str.upper(place.country[:2])
        place.save()
        return HttpResponseRedirect(self.get_success_url())


class ChangePlace(BaseChangeView):
    model = Place
    fields = ['name', 'contact_type', 'website', 'languages', 'who_lives_here', 'currency',
              'picture', 'description', 'outdoor_place', 'wifi', 'separate_entrance', 'common_kitchen',
              'pick_up_service', 'parking', 'own_key', 'laundry', 'meals', 'meal_example',
              'vegan', 'vegetarian', 'check_in_time', 'check_out_time', 'id']
    template_name = 'places/create_place.html'

    def get_context_data(self, **kwargs):
        """add the detail lists"""
        kwargs['rooms'] = self.object.room_set.all()
        kwargs['prices'] = self.object.price_set.all()
        kwargs['admins'] = User.objects.filter(placeaccount__place=self.object)
        kwargs['place_id'] = self.object.id
        return super().get_context_data(**kwargs)


class BaseCreateView(LoginRequiredWithURL, UserPassesTestMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'places.change_place'

    def get_place_id(self):
        return self.kwargs['pk']

    def get_success_url(self):
        return reverse('places:detail', kwargs={'pk': self.get_place_id()})

    def form_valid(self, form):
        new_model = form.save(commit=False)
        new_model.place_id = self.get_place_id()
        new_model.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return PlaceAccount.edit_place_permission(self.request.user, self.get_place_id())


class CreatePrice(BaseCreateView):
    model = Price
    fields = ['description', 'category', 'value']
    template_name = 'places/create_detail.html'


class CreateRoom(BaseCreateView):
    model = Room
    fields = ['room_number', 'beds', 'bathroom', 'kitchen', 'outdoor_place', 'room_add', 'smoking', 'pets', 'family',
              'handicapped_enabled', 'price_per_person', 'price_per_room', 'valid_from', 'valid_to']
    template_name = 'places/create_detail.html'


class PlaceCategoryForm(ModelForm):
    """form for the minimum of information creating a new place"""
    TINY = "TI"
    SMALL = "SM"
    MEDIUM = "ME"
    LARGE = "LA"
    HOTEL = "HO"
    NOT_AVAILABLE = "NA"
    HOST_CATEGORY = ((TINY, "One room to rent with 2 beds"), (SMALL, "Two rooms with 2-3 beds"),
                     (MEDIUM, "Three rooms with 2-6 beds"), (LARGE, "Four rooms with 2-6 beds"),
                     (HOTEL, "More than four rooms to rent "), (NOT_AVAILABLE, "n/a"))

    breakfast_included = forms.BooleanField(required=False)
    std_price = forms.DecimalField(decimal_places=2, label="Standard price for one night and one person")
    category = forms.ChoiceField(choices=HOST_CATEGORY)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['country'] = str.upper(self.cleaned_data.get('country', ''))
        logger.debug(cleaned_data)
        return cleaned_data

    class Meta:
        model = Place
        fields = ['name', 'picture', 'country']


class CreatePlaceMinimal(LoginRequiredWithURL, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'places.add_place'
    form_class = PlaceCategoryForm
    model = Place
    initial = {'breakfast_included': True, 'std_price': 30.0, 'category': Categories.TINY}
    template_name = 'places/create_place_minimal.html'
    context_object_name = 'form'

    @atomic
    def form_valid(self, form):
        logger.debug(self.request.POST)
        place = form.save(commit=False)
        place.created_by = self.request.user
        place.save()
        place.add_std_rooms_and_prices(form.cleaned_data['category'], form.cleaned_data['std_price'])
        # todo: what to do with breakfast included
        PlaceAccount.objects.create(place_id=place.id, user_id=self.request.user.id)
        return HttpResponseRedirect(reverse('places:detail', kwargs={'pk': place.id}))
