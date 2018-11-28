from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from traveller.views import register_user, register_worker, update_traveller, login_user

app_name = 'traveller'
urlpatterns = [
                  path('register/<int:place_id>/', register_user, name='register-user'),
                  path('register/', register_worker, name='register-worker'),
                  path('user/<int:place_id>/<int:user_id>/', update_traveller, name='create-user'),
                  path('login/', login_user, name='traveller-login'),
                  path('logout/', admin.site.logout, name='traveller-logout'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
