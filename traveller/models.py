# import the logging library
import logging

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, Group
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from places.models import Place

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.screen_name = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={
                                  'unique': _("This email already exists."),
                              },
                              )
    full_name = models.CharField(_('full name'), max_length=128, blank=True)
    screen_name = models.CharField(_('screen name'), max_length=32, blank=True, db_index=True)
    unique_name = models.CharField(_('unique name'), max_length=64, unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    picture = models.ImageField(blank=True, null=True)
    alt_email = models.EmailField(blank=True, null=True)
    street = models.CharField(blank=True, null=True, max_length=128)
    city = models.CharField(blank=True, null=True, max_length=128)
    zip = models.CharField(blank=True, null=True, max_length=32)
    country = models.CharField(blank=True, null=True, max_length=2)
    state = models.CharField(blank=True, null=True, max_length=2)
    vita = models.TextField(blank=True, null=True, max_length=1024)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. '
                                        'Unselect this instead of deleting accounts.'
                                    ),
                                    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        """Return screen name of the."""
        if self.screen_name == self.unique_name:
            return self.screen_name
        return f"{self.screen_name}({self.unique_name})"

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def create_screen_names(self):
        """Screen name could be set and will be displayed in any posts to avoid publishing the email address.
        If screen name is not unique the unique name is added in brackets. See property display_name"""
        if self.unique_name is not None:
            return
        if self.screen_name is None or self.screen_name == '':
            return
        other_screen_user_names = User.objects.filter(screen_name__exact=self.screen_name)
        logger.debug(other_screen_user_names)
        if other_screen_user_names is None or other_screen_user_names.count() == 0:
            self.unique_name = self.screen_name
            return
        self.unique_name = ''.join([self.screen_name, str(self.id)])

    @property
    def display_name(self) -> str:
        if self.unique_name is not None and self.unique_name != '':
            if self.unique_name != self.screen_name:
                return f"{self.screen_name} ({self.unique_name})"
            return self.screen_name
        return self.email

    @property
    def display_name_html(self) -> str:
        if self.unique_name is not None and self.unique_name != '':
            if self.unique_name != self.screen_name:
                return f'<div class="screen-user-name-display">{self.screen_name}</div>' \
                    f'<div class="unique-user-name-display">({self.unique_name})</div>'
            return f'<div class="screen-user-name-display">{self.screen_name}<div>'
        removed_at = self.email.replace('@', ' AT ')
        return f'<div class="screen-user-name-display">{removed_at}<div>'

    @property
    def is_place_admin(self) -> bool:
        return Group.objects.filter(name__iexact='PlaceAdmin', user=self).count() > 0

    @property
    def is_traveller(self) -> bool:
        return Group.objects.filter(name__iexact='Traveller', user=self).count() > 0

    @property
    def is_worker(self) -> bool:
        return Group.objects.filter(name__iexact='Worker', user=self).count() > 0

    def __str__(self):
        return self.display_name


class PlaceAccount(models.Model):
    place = models.ForeignKey(to=Place, null=True, blank=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} <-> {self.place.name}"
