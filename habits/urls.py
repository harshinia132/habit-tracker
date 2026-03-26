from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/habits/', views.api_habits, name='api_habits'),
    path('api/habits/<int:habit_id>/', views.api_habit_detail, name='api_habit_detail'),
    path('api/habits/<int:habit_id>/checkins/', views.api_checkins, name='api_checkins'),
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/sync/', views.api_sync, name='api_sync'),
]