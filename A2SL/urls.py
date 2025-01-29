from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('animation/', views.animation_view, name='animation'),
    path('record/', views.record_video_audio, name='record_video_audio'),
    path('logout/', views.logout_view, name='logout'),
]
