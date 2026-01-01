from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MuscleGroup(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  active = models.BooleanField(default=True)
  image_url = models.URLField(
    max_length=500,
    null=True,
    blank=True,
    help_text="URL de la imagen del grupo muscular"
  )

  def __str__(self):
      return self.name

class ExerciseType(models.Model):
  name = models.CharField(max_length=50)
  active = models.BooleanField(default=True)

  def __str__(self):
    return self.name
  
class Exercise(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT)
  exercise_type = models.ForeignKey(ExerciseType, on_delete=models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True)
  image_url = models.URLField(
    max_length=500,
    null=True,
    blank=True,
    help_text="URL de la imagen del ejercicio"
  )

  def __str__(self):
    return self.name
    
class Routine(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routines')
  name = models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.name} - {self.user.username}"

class RoutineItem(models.Model):
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='items')
  exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
  order = models.PositiveIntegerField()
  target_sets = models.PositiveIntegerField(default=4)
  target_reps = models.PositiveIntegerField(default=10)
  rest_time_seconds = models.PositiveIntegerField(default=60)

  class Meta:
    ordering = ['order']
    unique_together = [['routine', 'order']]

  def __str__(self):
    return f"{self.exercise.name} en {self.routine.name}"
  
class WorkoutSession(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
  routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, null=True, blank=True)
  start_time = models.DateTimeField(auto_now_add=True)
  end_time = models.DateTimeField(null=True, blank=True)

  @property
  def is_active(self):
    return self.end_time is None
  
  @property
  def duration_minutes(self):
    if self.end_time:
      delta = self.end_time - self.start_time
      return int(delta.total_seconds() / 60)
    return None

  def __str__(self):
    return f"Sesión {self.id} - {self.user.username} - {self.start_time.date()}"

class WorkoutSet(models.Model):
  session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
  exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
  set_number = models.PositiveIntegerField()
  weight = models.DecimalField(max_digits=6, decimal_places=2)
  reps = models.PositiveIntegerField()
  completed_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['completed_at']
    indexes = [
      models.Index(fields=['session', 'exercise']),
      models.Index(fields=['exercise', '-completed_at']),
    ]

  def __str__(self):
    return f"Set {self.set_number}: {self.weight}kg x {self.reps} - {self.exercise.name}"

class DayOfWeek(models.IntegerChoices):
  LUNES = 0, "Lunes"
  MARTES = 1, "Martes"
  MIERCOLES = 2, "Miércoles"
  JUEVES = 3, "Jueves"
  VIERNES = 4, "Viernes"
  SABADO = 5, "Sábado"
  DOMINGO = 6, "Domingo"

class RoutineSchedule(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
  routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='schedules')
  day_of_week = models.IntegerField(choices=DayOfWeek.choices)
  
  class Meta:
    unique_together = ['user', 'day_of_week'] 
    ordering = ['day_of_week']

  def __str__(self):
    return f"{self.get_day_of_week_display()}: {self.routine.name} ({self.user.username})"