from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from traveller.views import update_traveller, register_user, register_worker
from . import views
from .forms import DetailView, IndexView, EditRoom, EditPrice, DeletePrice, DeleteRoom, EditPlaceAddressView

app_name = 'places'
urlpatterns = \
    [
        path('', IndexView.as_view(), name='index'),
        path('new/', views.create_new_place, name='create-place'),
        path('price/<int:place>/', views.create_new_price, name='create-price'),
        path('register/<int:place_id>/', register_user, name='register-user'),
        path('register/', register_worker, name='register-worker'),
        path('user/<int:place_id>/<int:user_id>/', update_traveller, name='create-user'),
        path('room/<int:place>/', views.create_new_room, name='create-room'),
        path('<int:pk>/', DetailView.as_view(), name='detail'),
        path('update/place/<int:pk>/', views.update_place, name='update-place'),
        path('update/place/address/<int:pk>/', EditPlaceAddressView.as_view(), name='update-place-address'),
        path('update/room/<int:pk>/', EditRoom.as_view(), name='update-room'),
        path('update/price/<int:pk>/', EditPrice.as_view(), name='update-price'),
        path('delete/room/<int:pk>/', DeleteRoom.as_view(), name='delete-room'),
        path('delete/price/<int:pk>/', DeletePrice.as_view(), name='delete-price'),
        path('base_layout', views.base_layout, name='base_layout'),
        path('intro/', views.show_intro, name='intro'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
