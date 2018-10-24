from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'places'
urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('new/', views.create_new_place, name='new'),
                  path('price/<int:place>/', views.create_new_price, name='create_price'),
                  path('user/<int:place_id>/', views.add_administrator_to_place, name='add_user'),
                  path('room/<int:place>/', views.create_new_room, name='create_room'),
                  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
                  path('update/<int:pk>/', views.update_place, name='update_place'),
                  path('base_layout', views.base_layout, name='base_layout'),
                  path('intro/', views.show_intro, name='intro'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
