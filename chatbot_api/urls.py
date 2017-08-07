from django.conf.urls import url
from chatbot_api import views

urlpatterns = [
    url(r'^hello_world$', views.hello_world)
    ]
