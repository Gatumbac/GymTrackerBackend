from rest_framework import serializers
from .models import MuscleGroup, ExerciseType, Exercise

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

        