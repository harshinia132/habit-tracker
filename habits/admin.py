from django.contrib import admin
from .models import Habit, Checkin

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'frequency', 'is_active', 'created_at']
    list_filter = ['frequency', 'is_active']
    search_fields = ['name']

@admin.register(Checkin)
class CheckinAdmin(admin.ModelAdmin):
    list_display = ['habit', 'date', 'completed']
    list_filter = ['completed', 'date']