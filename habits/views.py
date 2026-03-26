from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from .models import Habit, Checkin

def index(request):
    """Main view for the habit tracker"""
    return render(request, 'habits/index.html')

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_habits(request):
    """API endpoint for habits"""
    if request.method == 'GET':
        habits = Habit.objects.all()
        if request.user.is_authenticated:
            habits = habits.filter(user=request.user)
        data = []
        for habit in habits:
            data.append({
                'id': habit.id,
                'name': habit.name,
                'description': habit.description,
                'frequency': habit.frequency,
                'target_days': habit.target_days,
                'is_active': habit.is_active,
                'reminder_time': str(habit.reminder_time) if habit.reminder_time else None,
                'reminder_enabled': habit.reminder_enabled,
                'current_streak': habit.get_current_streak(),
                'longest_streak': habit.get_longest_streak(),
                'created_at': habit.created_at.isoformat(),
            })
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        habit = Habit.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            frequency=data.get('frequency', 'daily'),
            target_days=data.get('target_days', 1),
            reminder_time=data.get('reminder_time'),
            reminder_enabled=data.get('reminder_enabled', False),
        )
        if request.user.is_authenticated:
            habit.user = request.user
            habit.save()
        return JsonResponse({
            'id': habit.id,
            'name': habit.name,
            'message': 'Habit created successfully'
        }, status=201)

@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def api_habit_detail(request, habit_id):
    """API endpoint for single habit"""
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return JsonResponse({'error': 'Habit not found'}, status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body)
        habit.name = data.get('name', habit.name)
        habit.description = data.get('description', habit.description)
        habit.frequency = data.get('frequency', habit.frequency)
        habit.target_days = data.get('target_days', habit.target_days)
        habit.is_active = data.get('is_active', habit.is_active)
        habit.reminder_time = data.get('reminder_time', habit.reminder_time)
        habit.reminder_enabled = data.get('reminder_enabled', habit.reminder_enabled)
        habit.save()
        return JsonResponse({'message': 'Habit updated successfully'})
    
    elif request.method == 'DELETE':
        habit.delete()
        return JsonResponse({'message': 'Habit deleted successfully'})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_checkins(request, habit_id):
    """API endpoint for checkins"""
    try:
        habit = Habit.objects.get(id=habit_id)
    except Habit.DoesNotExist:
        return JsonResponse({'error': 'Habit not found'}, status=404)
    
    if request.method == 'GET':
        checkins = habit.checkin_set.all().order_by('-date')
        data = [{
            'id': c.id,
            'date': c.date.isoformat(),
            'completed': c.completed,
            'notes': c.notes
        } for c in checkins]
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        checkin, created = Checkin.objects.get_or_create(
            habit=habit,
            date=data.get('date', timezone.now().date()),
            defaults={'completed': data.get('completed', False)}
        )
        if not created:
            checkin.completed = data.get('completed', checkin.completed)
            checkin.notes = data.get('notes', checkin.notes)
            checkin.save()
        return JsonResponse({
            'id': checkin.id,
            'message': 'Checkin saved successfully'
        })

@require_http_methods(["GET"])
def api_stats(request):
    """API endpoint for statistics"""
    habits = Habit.objects.all()
    if request.user.is_authenticated:
        habits = habits.filter(user=request.user)
    
    stats = []
    for habit in habits:
        checkins = habit.checkin_set.filter(completed=True).order_by('date')
        stats.append({
            'habit_id': habit.id,
            'habit_name': habit.name,
            'current_streak': habit.get_current_streak(),
            'longest_streak': habit.get_longest_streak(),
            'total_checkins': checkins.count(),
            'completion_rate': (checkins.count() / 30) * 100 if checkins.count() > 0 else 0,
            'checkin_dates': [c.date.isoformat() for c in checkins]
        })
    
    return JsonResponse(stats, safe=False)

@require_http_methods(["POST"])
def api_sync(request):
    """Sync offline data with server"""
    data = json.loads(request.body)
    results = []
    
    for habit_data in data.get('habits', []):
        habit, created = Habit.objects.get_or_create(
            id=habit_data.get('id'),
            defaults={
                'name': habit_data['name'],
                'description': habit_data.get('description', ''),
                'frequency': habit_data.get('frequency', 'daily'),
                'target_days': habit_data.get('target_days', 1),
            }
        )
        results.append({'habit_id': habit.id, 'created': created})
    
    for checkin_data in data.get('checkins', []):
        try:
            habit = Habit.objects.get(id=checkin_data['habit_id'])
            checkin, created = Checkin.objects.get_or_create(
                habit=habit,
                date=checkin_data['date'],
                defaults={'completed': checkin_data['completed']}
            )
            results.append({'checkin_id': checkin.id, 'created': created})
        except Habit.DoesNotExist:
            continue
    
    return JsonResponse({'message': 'Sync completed', 'results': results})