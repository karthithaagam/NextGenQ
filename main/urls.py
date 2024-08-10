from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('practical/', views.msc_practical, name='practical'),
    path('upload/', views.imagetypeconverter, name='upload'),
]
