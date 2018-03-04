from django.urls import path

from revision import views

urlpatterns = [
    path('', views.planning, name='planning')
]
