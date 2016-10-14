from django.conf.urls import include, url
from django.contrib import admin
from . import views 

urlpatterns = [
    # Examples:
    # url(r'^$', 'makemymeal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',views.home, name='home'),
    url(r'^meals=(?P<days>[0-9&]+)/$', views.meals, name='meals'),
    url(r'^meals=(?P<current>[0-9&]+)/new_recipe$', views.new_recipe, name='new_recipe'),
    url(r'meals=(?P<current>[0-9&]+)/nah$',views.nah,name='nah'),
    url(r'^newAjax$',views.newRecipeAjax,name='newRecipeAjax'),
    url(r'^new$', views.new, name='new'),
]
