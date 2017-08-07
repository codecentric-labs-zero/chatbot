from django.conf.urls import url
from chatbot_web import views

# patterns here are prefixed with 'web/'
urlpatterns = [
    url(r'^ping$', views.ping),
    url(r'^ask', views.ask),
    url(r'^$', views.hello_world)
    ]
