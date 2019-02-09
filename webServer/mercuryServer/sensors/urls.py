from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/', views.get, name='get'),
    path('update/<str:dictionary>', views.update, name='update')
]