from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from rango import views

# Class that redirects the user to the index page,
# if successful at logging
class CustomRegistrationView(RegistrationView):
    def get_success_url(self, view):
        return '/rango/'


urlpatterns = [
    url(r'^rango/', include('rango.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', CustomRegistrationView.as_view(),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
