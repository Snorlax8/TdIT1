from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/<int:movie_id>/', views.detail, name='detail'),
    path('characters/<int:character_id>/', views.character_detail, name='character_detail'),
    path('ships/<int:starship_id>/', views.ship_detail, name='ship_detail'),
    path('planets/<int:planet_id>/', views.planet_detail, name='planet_detail'),
    path('search/', views.search),
]
