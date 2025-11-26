from django.urls import path

from . import views

app_name = "certificates"

urlpatterns = [
    path("", views.home, name="home"),
    path("api/chatkit/session/", views.create_chatkit_session, name="chatkit_session"),
]


