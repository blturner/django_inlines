from django.conf.urls import include, url
from django.contrib import admin

from .models import User

admin.site.register(User)

urlpatterns = [
    url(r'^admin/inlines/', include('django_inlines.admin_urls')),
    url(r'^admin/', include(admin.site.urls)),
]
