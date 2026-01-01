from rest_framework import serializers
from .models import MuscleGroup, ExerciseType, Exercise, Routine, RoutineItem

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

        