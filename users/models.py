from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name="profile")
  birth_date = models.DateField(null=True, blank=True)
  height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
  weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
  avatar = models.URLField(
    max_length=500,
    null=True,
    blank=True,
    help_text="URL de la imagen del avatar"
  )
  bio = models.TextField(max_length=500, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Perfil de {self.user.username}"
  
  @property
  def is_complete(self):
      return all([self.birth_date, self.height, self.weight])