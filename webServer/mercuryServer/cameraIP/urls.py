from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('update/<str:newIP>/', views.update, name='update')
]