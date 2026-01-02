from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (MuscleGroupViewSet, 
                    ExerciseTypeViewSet, 
                    ExerciseViewSet, 
                    RoutineViewSet, 
                    RoutineScheduleViewSet, 
                    WorkoutSetViewSet,
                    WorkoutSessionViewSet)

router = DefaultRouter()
router.register(r'muscle-groups', MuscleGroupViewSet)
router.register(r'exercise-types', ExerciseTypeViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'routines', RoutineViewSet, basename='routine')
router.register(r'routine-schedules', RoutineScheduleViewSet, basename='routine-schedule')
router.register(r'workout-sessions', WorkoutSessionViewSet, basename='workout-session')
router.register(r'workout-sets', WorkoutSetViewSet, basename='workout-set')

app_name = 'exercises'
urlpatterns = [
  path('', include(router.urls))
]