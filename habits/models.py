from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    target_days = models.IntegerField(default=1)  # Target per frequency period
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    reminder_time = models.TimeField(null=True, blank=True)
    reminder_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def get_current_streak(self):
        """Calculate current streak"""
        checkins = self.checkin_set.filter(
            completed=True
        ).order_by('-date')
        
        if not checkins:
            return 0
            
        streak = 0
        current_date = timezone.now().date()
        
        for checkin in checkins:
            if checkin.date == current_date or \
               (checkin.date == current_date - timezone.timedelta(days=streak)):
                streak += 1
            else:
                break
                
        return streak
    
    def get_longest_streak(self):
        """Calculate longest streak"""
        checkins = self.checkin_set.filter(
            completed=True
        ).order_by('date')
        
        if not checkins:
            return 0
            
        longest = 0
        current = 1
        
        for i in range(1, len(checkins)):
            if (checkins[i].date - checkins[i-1].date).days == 1:
                current += 1
            else:
                longest = max(longest, current)
                current = 1
                
        return max(longest, current)

class Checkin(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['habit', 'date']
        
    def __str__(self):
        return f"{self.habit.name} - {self.date}"