import logging

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import EmailField
from django.forms.models import modelform_factory
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from traveller.models import User, PlaceAccount

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class ChangeUser(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = User
    template_name = 'traveller/create_place_admin.html'
    form_class = modelform_factory(User, widgets={'groups': forms.widgets.CheckboxSelectMultiple()},
                                   exclude=['password', 'user_permissions', 'last_login'])
    login_url = '/traveller/login/'

    def test_func(self):
        place_id = self.get_place_id()
        if place_id == 0:
            return self.request.user.is_staff
        return PlaceAccount.edit_place_permission(self.request.user, place_id)

    def get_place_id(self):
        for key in ('place', 'place_id'):
            if key in self.kwargs:
                logger.debug(f'Place id from {key} parameter is {self.kwargs[key]}')
                return self.kwargs[key]
        return 0

    def get_success_url(self):
        place_id = self.get_place_id()
        if place_id > 0:
            return reverse('places:detail', kwargs={'pk': place_id})
        return reverse('admin:index')


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
