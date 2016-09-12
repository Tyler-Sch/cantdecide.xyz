from django.conf.urls import include, url

urlpatterns = [
    # Examples:
    # url(r'^$', 'makemymeal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'views.home', name='home'),
]
