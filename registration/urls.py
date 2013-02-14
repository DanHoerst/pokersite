from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^register/', views.UserRegistration, name="register"),
    url(r'^login/$', views.LoginRequest, name="login"),
    url(r'^logout/$', views.LogoutRequest, name="logout"),
    url(r'^mailreset/$', views.PasswordReset, name="passwordreset")
)
