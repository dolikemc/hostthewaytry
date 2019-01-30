from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from booking.forms import BookingCreate

app_name = 'booking'
urlpatterns = \
    [
        path('new/<int:pk>/', BookingCreate.as_view(), name='create-booking'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
