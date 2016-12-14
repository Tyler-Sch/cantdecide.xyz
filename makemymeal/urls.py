from django.conf.urls import include, url
from django.contrib import admin
from youdecide import urls as youdecide_urls

urlpatterns = [
    url(r'^youdecide/', include(youdecide_urls)),
    url(r'^admin/', include(admin.site.urls)),]

