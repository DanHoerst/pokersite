from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^new/new_screenname/(?P<player_id>[\w|\W]+)/', views.new_screename, name="new_screename"),
    url(r'^new/new_session/(?P<screename_id>[\w|\W]+)/', views.new_session, name="new_session"),
    url(r'^$', views.player_list, name="player_list"),
    url(r'^player/(?P<player_id>[\w|\W]+)/', views.screename_list, name="screename_list"),
    url(r'^screenname/(?P<screename_id>[\w|\W]+)/', views.session_list, name="session_list"),
)