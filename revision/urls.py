from django.urls import path

from revision import views

urlpatterns = [
    path('', views.home, name='home')
]
