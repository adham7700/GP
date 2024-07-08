from django.urls import path
from . import views


urlpatterns = [
     path('about/', views.report,name='blog-report'),  # / -> home
    path('', views.home,name='blog-home'),
]