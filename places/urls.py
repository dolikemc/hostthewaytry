from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from places import views, forms

app_name = 'places'
urlpatterns = \
    [
        path('', forms.IndexView.as_view(), name='index'),
        path('history/', forms.IndexHistoryView.as_view(), name='history'),
        path('filter/', forms.IndexFilterView.as_view(), name='filter'),
        path('worker/', forms.IndexWorkerView.as_view(), name='worker'),
        path('place_admin/', forms.IndexPlaceAdminView.as_view(), name='place_admin'),
        path('new/', forms.CreatePlaceMinimal.as_view(), name='create-place'),
        path('price/<int:pk>/', forms.CreatePrice.as_view(), name='create-price'),
        path('room/<int:pk>/', forms.CreateRoom.as_view(), name='create-room'),
        path('<int:pk>/', forms.DetailView.as_view(), name='detail'),
        path('update/place/<int:pk>/', forms.ChangePlace.as_view(), name='update-place'),
        path('update/place/address/<int:pk>/', forms.ChangePlaceAddress.as_view(), name='update-place-address'),
        path('update/room/<int:pk>/', forms.ChangeRoom.as_view(), name='update-room'),
        path('update/price/<int:pk>/', forms.ChangePrice.as_view(), name='update-price'),
        path('delete/room/<int:pk>/', forms.DeleteRoom.as_view(), name='delete-room'),
        path('delete/place/<int:pk>/', views.delete_place, name='delete-place'),
        path('undelete/place/<int:pk>/', views.undelete_place, name='un-delete-place'),
        path('delete/price/<int:pk>/', forms.DeletePrice.as_view(), name='delete-price'),
        path('intro/', views.show_intro, name='intro'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
