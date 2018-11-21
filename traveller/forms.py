from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Traveller


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class TravellerForm(ModelForm):
    class Meta:
        model = Traveller
        fields = ['alt_email', 'street', 'country', 'zip', 'city', 'state',
                  'picture', 'vita']


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
