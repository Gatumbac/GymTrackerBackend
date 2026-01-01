from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import MuscleGroup, ExerciseType, Exercise
from .serializers import MuscleGroupSerializer, ExerciseTypeSerializer, ExerciseSerializer

# Create your views here.
class MuscleGroupViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = MuscleGroup.objects.all()
  serializer_class = MuscleGroupSerializer

class ExerciseTypeViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = ExerciseType.objects.all()
  serializer_class = ExerciseTypeSerializer

class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Exercise.objects.select_related('muscle_group', 'exercise_type').all()
  serializer_class = ExerciseSerializer
  permission_classes = []
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['muscle_group', 'exercise_type']