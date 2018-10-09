from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'places'
urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('add/', views.create_new_place, name='create'),
                  path('price/', views.create_new_price, name='create_price'),
                  path('room/', views.create_new_room, name='create_room'),
                  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
                  path('change/<int:pk>/', views.update_place, name='change_place'),
                  path('base_layout', views.base_layout, name='base_layout'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
