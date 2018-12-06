from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from traveller.forms import ChangeUser
from traveller.views import register_user, login_user

app_name = 'traveller'
urlpatterns = [
                  path('register/<int:place_id>/', register_user, name='register-user'),
                  path('register/', register_user, name='register-worker'),
                  path('user/<int:pk>/<int:place_id>/', ChangeUser.as_view(), name='create-user'),
                  # path('update/user/<int:pk>/', ChangeUser.as_view(), name='change-user'),
                  path('login/', login_user, name='traveller-login'),
                  path('logout/', admin.site.logout, name='traveller-logout'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
