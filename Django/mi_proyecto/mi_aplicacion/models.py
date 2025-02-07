from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    propietario = models.ForeignKey(User, on_delete = models.CASCADE)
    completada = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titulo
