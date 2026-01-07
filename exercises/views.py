from django.db import models
from django.utils import timezone
from rest_framework import viewsets, status, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (MuscleGroup, 
                     ExerciseType, 
                     Exercise, 
                     Routine, 
                     RoutineSchedule, 
                     DayOfWeek, 
                     WorkoutSession, 
                     WorkoutSet)
from .serializers import (MuscleGroupSerializer, 
                          ExerciseTypeSerializer, 
                          ExerciseSerializer, 
                          RoutineSerializer, 
                          RoutineScheduleSerializer, 
                          WorkoutSessionSerializer, 
                          WorkoutSetSerializer)

# Create your views here.
class MuscleGroupViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = MuscleGroup.objects.all()
  serializer_class = MuscleGroupSerializer

class ExerciseTypeViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = ExerciseType.objects.all()
  serializer_class = ExerciseTypeSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
  # optimizacion de query. Uso de select related para evitar N+1 queries y reducirla a una sola
  queryset = Exercise.objects.select_related('muscle_group', 'exercise_type').all()
  serializer_class = ExerciseSerializer
  permission_classes = []
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['muscle_group', 'exercise_type']

  def get_queryset(self):
    return Exercise.objects.select_related('muscle_group', 'exercise_type').filter(
      models.Q(user=self.request.user) | models.Q(user__isnull=True)
    )

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class RoutineViewSet(viewsets.ModelViewSet):
  serializer_class = RoutineSerializer

  # optimizacion de query. Uso de prefetch related para evitar N+1 queries y reducirla a solo 3
  def get_queryset(self):
    return Routine.objects.filter(user=self.request.user).prefetch_related('items__exercise').order_by('-created_at')
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
  
class RoutineScheduleViewSet(viewsets.ModelViewSet):
  serializer_class = RoutineScheduleSerializer

  # optimizacion de query. Uso de select related para evitar N+1 queries y reducirla a una sola
  def get_queryset(self):
    return RoutineSchedule.objects.filter(user=self.request.user).select_related('routine').order_by('day_of_week')
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  @action(detail=False, methods=['get'])
  def weekly(self, request):
    schedules = self.get_queryset()
    schedule_map = {s.day_of_week: s for s in schedules}
    weekly_data = []

    for day_code, day_label in DayOfWeek.choices:
      schedule = schedule_map.get(day_code)
      if schedule:
        data = RoutineScheduleSerializer(schedule).data
      else: 
        data = None
      
      weekly_data.append({
        "day_of_week": day_code,
        "day_name": day_label,
        "schedule": data
      })

    return Response(weekly_data)

class WorkoutSessionViewSet(viewsets.ModelViewSet):
  serializer_class = WorkoutSessionSerializer

  def get_queryset(self):
    return WorkoutSession.objects.filter(user=self.request.user).prefetch_related('sets__exercise').order_by('-start_time')
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
  
  @action(detail=False, methods=['get'])
  def active(self, request):
    active_session = WorkoutSession.objects.filter(user=request.user, end_time__isnull=True).prefetch_related('sets__exercise').first()
      
    if active_session:
      serializer = self.get_serializer(active_session)
      return Response(serializer.data)
      
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  @action(detail=True, methods=['post'])
  def complete(self, request, pk=None):
    session = self.get_object() 
    
    if session.end_time:
      return Response({"error": "Esta sesión ya estaba finalizada."}, status=status.HTTP_400_BAD_REQUEST)

    session.end_time = timezone.now()
    session.save()
    
    serializer = self.get_serializer(session)
    return Response(serializer.data)

class WorkoutSetViewSet(mixins.CreateModelMixin, 
                        mixins.RetrieveModelMixin, 
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin, 
                        viewsets.GenericViewSet):
  serializer_class = WorkoutSetSerializer
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['session', 'exercise']

  def get_queryset(self):
    return WorkoutSet.objects.filter(session__user=self.request.user).select_related('exercise', 'session').order_by('-completed_at')


  

