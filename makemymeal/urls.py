from django.conf.urls import include, url
from django.contrib import admin
import youdecide

urlpatterns = [
    # Examples:
    # url(r'^$', 'makemymeal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^youdecide/$','youdecide.views.home', name='home'),
    url(r'^youdecide/meals=(?P<days>[0-9&]+)/$', 'youdecide.views.meals', name='meals'),
    url(r'^youdecide/meals=(?P<current>[0-9&]+)/new_recipe$', 'youdecide.views.new_recipe', name='new_recipe'),
    url(r'youdecide/meals=(?P<current>[0-9&]+)/nah$','youdecide.views.nah',name='nah'),
    url(r'^youdecide/new$', 'youdecide.views.new', name='new'),
    url(r'^admin/', include(admin.site.urls)),
]
