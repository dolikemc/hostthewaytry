from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from places import views
from places.forms import DetailView, IndexView, ChangeRoom, ChangePrice, DeletePrice, DeleteRoom, ChangePlaceAddress, \
    IndexPlaceAdminView, IndexWorkerView, CreatePrice, CreateRoom

app_name = 'places'
urlpatterns = \
    [
        path('', IndexView.as_view(), name='index'),
        path('worker', IndexWorkerView.as_view(), name='worker'),
        path('place_admin', IndexPlaceAdminView.as_view(), name='place_admin'),
        path('new/', views.create_new_place, name='create-place'),
        path('price/<int:pk>/', CreatePrice.as_view(), name='create-price'),
        path('room/<int:pk>/', CreateRoom.as_view(), name='create-room'),
        path('<int:pk>/', DetailView.as_view(), name='detail'),
        path('update/place/<int:pk>/', views.update_place, name='update-place'),
        path('update/place/address/<int:pk>/', ChangePlaceAddress.as_view(), name='update-place-address'),
        path('update/room/<int:pk>/', ChangeRoom.as_view(), name='update-room'),
        path('update/price/<int:pk>/', ChangePrice.as_view(), name='update-price'),
        path('delete/room/<int:pk>/', DeleteRoom.as_view(), name='delete-room'),
        path('delete/place/<int:pk>/', DeletePrice.as_view(), name='delete-place'),
        path('undelete/place/<int:pk>/', DeletePrice.as_view(), name='undelete-place'),
        path('delete/price/<int:pk>/', DeletePrice.as_view(), name='delete-price'),
        path('base_layout', views.base_layout, name='base_layout'),
        path('intro/', views.show_intro, name='intro'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
