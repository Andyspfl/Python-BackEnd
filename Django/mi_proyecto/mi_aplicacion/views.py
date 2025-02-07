from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Tarea
from .serializers import TareaSerializer

# Create your views here.

class TareaListCreate(generics.ListCreateAPIView):
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Tarea.objects.filter(propietario = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(propietario = self.request.user)
        
class TareaDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Tarea.objects.filter(propietario = self.request.user)
    