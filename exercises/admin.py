from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Exercise)
admin.site.register(ExerciseType)
admin.site.register(MuscleGroup)
admin.site.register(Routine)
admin.site.register(RoutineItem)
admin.site.register(WorkoutSession)
admin.site.register(WorkoutSet)
admin.site.register(RoutineSchedule)
