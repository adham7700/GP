from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
   path('video_feed', views.video_feed, name='video_feed'),
   path('translate/', views.trans, name='translate'),
   path('translatee/', views.translate, name='translatee'),
   path('answer/', views.zyadaa, name='zyadaa'),
    path('get_result', views.get_result, name='get_result'),

]