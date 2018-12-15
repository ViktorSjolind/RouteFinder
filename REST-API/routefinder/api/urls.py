from django.urls import path

from . import views

urlpatterns = [
    path('routes/', views.unofficial_routes),
]