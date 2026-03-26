from rest_framework import serializers
from .models import Habit, Checkin

class HabitSerializer(serializers.ModelSerializer):
    current_streak = serializers.SerializerMethodField()
    longest_streak = serializers.SerializerMethodField()
    
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'frequency', 'target_days', 
                 'created_at', 'is_active', 'reminder_time', 'reminder_enabled',
                 'current_streak', 'longest_streak']
    
    def get_current_streak(self, obj):
        return obj.get_current_streak()
    
    def get_longest_streak(self, obj):
        return obj.get_longest_streak()

class CheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkin
        fields = ['id', 'habit', 'date', 'completed', 'notes']