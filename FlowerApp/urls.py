from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('order/', views.order),
    path('catalog/', views.catalog),
]