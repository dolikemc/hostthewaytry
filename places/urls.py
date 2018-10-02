from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'places'
urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('add/', views.CreatePlace.as_view(), name='create'),
                  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
                  path('base_layout', views.base_layout, name='base_layout'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
