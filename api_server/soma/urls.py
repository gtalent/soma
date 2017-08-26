
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from . import settings
from . import views

urlpatterns = [
    url(r'^authenticate/', views.authenticate_view),
    url(r'^auth_check/', views.auth_check),
    url(r'^admin/', admin.site.urls),
] + static('static', document_root='static_root') + static('images', document_root=settings.MEDIA_ROOT + '/images')

for pkg in settings.SOMA_APPS:
    urlpatterns.append(url(r'^' + pkg + '/', include(pkg + '.urls')))

if settings.CHURCH_NAME is not None:
    admin.site.site_header = settings.CHURCH_NAME + ' Administration'
else:
    admin.site.site_header = 'SaltDB Administration'
