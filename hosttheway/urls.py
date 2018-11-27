"""hosttheway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles import views
from django.urls import path, include
from django.views.generic import TemplateView

from places.forms import IndexPlaceAdminView, IndexWorkerView
from traveller.views import login_user

urlpatterns = [
                  path('', TemplateView.as_view(template_name='index.html')),
                  path('worker', IndexWorkerView.as_view(), name='worker'),
                  path('place_admin', IndexPlaceAdminView.as_view(), name='place_admin'),
                  path('legal.html', TemplateView.as_view(template_name='cookielaw/legal.html'), name='legal'),
                  path('admin/', admin.site.urls),
                  path('places/', include('places.urls')),
                  path('places/places/static/img/', views.serve),
                  path('accounts/login/', login_user, name='place-login'),
                  path('accounts/logout/', admin.site.logout, name='place-logout'),
              ] + static(settings.STATIC_URL, document_root=settings.BASE_DIR)
