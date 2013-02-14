from django.conf.urls import patterns, include, url
from django.contrib import admin



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stakeme.views.home', name='home'),
    # url(r'^stakeme/', include('stakeme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^', include('poker.urls')),
    url(r'^auth/', include('registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
