from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MuscleGroupViewSet, ExerciseTypeViewSet, ExerciseViewSet, RoutineViewSet

router = DefaultRouter()
router.register(r'muscle-groups', MuscleGroupViewSet)
router.register(r'exercise-types', ExerciseTypeViewSet)
router.register(r'exercises', ExerciseViewSet)
router.register(r'routines', RoutineViewSet, basename='routine')

app_name = 'exercises'
urlpatterns = [
  path('', include(router.urls))
]