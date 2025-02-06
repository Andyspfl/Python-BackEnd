from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from tasks import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet, 'tasks')
# Configura las rutas del router para tus vistas
urlpatterns = [
    path("api/v1/", include(router.urls)),  # Las rutas de tus vistas
    path("api/schema/", SpectacularAPIView.as_view(), name='schema'),  # Ruta para generar el esquema OpenAPI
    path("docs/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Ruta para acceder a la documentación Swagger
]