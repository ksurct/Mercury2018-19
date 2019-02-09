from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/<str:dictionary>/', views.update, name='update'),
    path('get/', views.get, name='get'),
]