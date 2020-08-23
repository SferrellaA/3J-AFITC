from django.http import HttpResponse
from django.conf.urls import url

def index(response):
    return HttpResponse("API page")

def test(response):
    return HttpResponse("test")

urlpatterns = [
    url('test/', test),
    url('', index),
]
