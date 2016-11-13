"""soma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from . import settings

urlpatterns = [
	url(r'^admin/', admin.site.urls),
] + static('static', document_root='static_root') + static('images', document_root='images')

for pkg in settings.SOMA_APPS:
	urlpatterns.append(url(r'^' + pkg + '/', include(pkg + '.urls')))

if settings.CHURCH_NAME is not None:
   admin.site.site_header = settings.CHURCH_NAME + ' Administration'
else:
   admin.site.site_header = 'Soma Administration'
