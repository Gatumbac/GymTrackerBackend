from rest_framework import serializers
from .models import (MuscleGroup, 
                     ExerciseType, 
                     Exercise, 
                     Routine, 
                     RoutineItem, 
                     RoutineSchedule, 
                     WorkoutSet, 
                     WorkoutSession)

class MuscleGroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = MuscleGroup
    fields = '__all__'

class ExerciseTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = ExerciseType
    fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
  muscle_group_name = serializers.CharField(source='muscle_group.name', read_only=True)
  exercise_type_name = serializers.CharField(source='exercise_type.name', read_only=True)
    
  class Meta:
    model = Exercise
    fields = ['id', 'name', 'description', 'image_url', 'muscle_group_name', 'exercise_type_name']
  
class RoutineItemSerializer(serializers.ModelSerializer):
  exercise_name = serializers.ReadOnlyField(source='exercise.name')
  exercise_image = serializers.ReadOnlyField(source='exercise.image_url')

  class Meta:
    model = RoutineItem
    fields = [
      'id',
      'exercise',
      'exercise_name',
      'exercise_image',
      'order',
      'target_sets',
      'target_reps',
      'rest_time_seconds'
    ]
    read_only_fields = ['id']

class RoutineSerializer(serializers.ModelSerializer):
  items = RoutineItemSerializer(many=True)

  class Meta:
    model = Routine
    fields = ['id', 'name', 'description', 'created_at', 'items']
    read_only_fields = ['id', 'created_at']
  
  def create(self, validated_data):
    items_data = validated_data.pop('items')
    routine = Routine.objects.create(**validated_data)

    for item_data in items_data:
      RoutineItem.objects.create(routine=routine, **item_data)

    return routine

  def update(self, instance, validated_data):
    items_data = validated_data.pop('items', None)
    instance.name = validated_data.get('name', instance.name)
    instance.description = validated_data.get('description', instance.description)
    instance.save()

    if (items_data is not None):
      instance.items.all().delete()
      for item_data in items_data:
        RoutineItem.objects.create(routine=instance, **item_data)
    
    return instance
  
class RoutineScheduleSerializer(serializers.ModelSerializer):
  routine_name = serializers.ReadOnlyField(source='routine.name')
  day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

  class Meta:
    model = RoutineSchedule
    fields = ['id', 'user', 'routine', 'routine_name', 'day_of_week', 'day_name']
    read_only_fields = ['id', 'user']

  # validar que la rutina pertenezca al usuario
  def validate_routine(self, value):
    user = self.context['request'].user
    if (value.user) != user:
      raise serializers.ValidationError("Rutina no pertenece al usuario")
    return value

class WorkoutSetSerializer(serializers.ModelSerializer):
  exercise_name = serializers.ReadOnlyField(source='exercise.name')
  exercise_image = serializers.ReadOnlyField(source='exercise.image_url')

  class Meta:
    model = WorkoutSet
    fields = ['id', 'session', 'exercise', 'exercise_name', 'exercise_image', 'set_number', 'weight', 'reps', 'completed_at']
    read_only_fields = ['id', 'completed_at']

  def validate_session(self, value):
    user = self.context['request'].user
    if value.user != user:
      raise serializers.ValidationError("Sesion no pertenece a usuario")
    if not value.is_active:
      raise serializers.ValidationError("Sesion finalizada")
    return value

class WorkoutSessionSerializer(serializers.ModelSerializer):
  sets = WorkoutSetSerializer(many=True, read_only=True)
  routine_name = serializers.ReadOnlyField(source='routine.name')
  duration = serializers.ReadOnlyField(source='duration_minutes')

  class Meta:
    model = WorkoutSession
    fields = ['id', 'routine', 'routine_name', 'start_time', 'end_time', 'is_active', 'duration', 'sets']
    read_only_fields = ['id', 'start_time', 'end_time', 'is_active', 'duration']