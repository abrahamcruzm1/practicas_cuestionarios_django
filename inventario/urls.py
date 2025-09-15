from django.urls import path
from . import views
from .views import (
    index,
    # Cuestionarios
    CuestionarioListView,

    CuestionarioCreateView,
    CuestionarioUpdateView,
    CuestionarioDeleteView,
    # Secciones
    SeccionListView,
    SeccionCreateView,
    SeccionUpdateView,
    SeccionDeleteView,
# Preguntas
    PreguntaListView,
    PreguntaCreateView,
    PreguntaUpdateView,
    PreguntaDeleteView,
    # Opciones
    OpcionRespuestaListView,
    OpcionRespuestaCreateView,
    OpcionRespuestaUpdateView,
    OpcionRespuestaDeleteView,
    # Clientes
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,

)

urlpatterns = [
    path("", index, name="index"),

    # CUESTIONARIOS
    path("cuestionarios/", CuestionarioListView.as_view(), name="cuestionarios-list"),

    path("cuestionarios/nuevo/", CuestionarioCreateView.as_view(), name="cuestionarios-create"),
    path("cuestionarios/<int:pk>/editar/", CuestionarioUpdateView.as_view(), name="cuestionarios-update"),
    path("cuestionarios/<int:pk>/borrar/", CuestionarioDeleteView.as_view(), name="cuestionarios-delete"),

    # SECCIONES
    path("cuestionarios/<int:cuestionario_id>/secciones/", SeccionListView.as_view(), name="secciones-list"),
    path("cuestionarios/<int:cuestionario_id>/secciones/nueva/", SeccionCreateView.as_view(), name="secciones-create"),
    path("secciones/<int:pk>/editar/", SeccionUpdateView.as_view(), name="secciones-update"),
    path("secciones/<int:pk>/borrar/", SeccionDeleteView.as_view(), name="secciones-delete"),

    # PREGUNTAS (ligadas a una sección)
    path("secciones/<int:seccion_id>/preguntas/", PreguntaListView.as_view(), name="preguntas-list"),
    path("secciones/<int:seccion_id>/preguntas/nueva/", PreguntaCreateView.as_view(), name="preguntas-create"),
    path("preguntas/<int:pk>/editar/", PreguntaUpdateView.as_view(), name="preguntas-update"),
    path("preguntas/<int:pk>/borrar/", PreguntaDeleteView.as_view(), name="preguntas-delete"),
    # OPCIONES (ligadas a una pregunta)
    path("preguntas/<int:pregunta_id>/opciones/", OpcionRespuestaListView.as_view(), name="opciones-list"),
    path("preguntas/<int:pregunta_id>/opciones/nueva/", OpcionRespuestaCreateView.as_view(), name="opciones-create"),
    path("opciones/<int:pk>/editar/", OpcionRespuestaUpdateView.as_view(), name="opciones-update"),
    path("opciones/<int:pk>/borrar/", OpcionRespuestaDeleteView.as_view(), name="opciones-delete"),

    # PREGUNTAS (ligadas a una sección)
    path("secciones/<int:seccion_id>/preguntas/", PreguntaListView.as_view(), name="preguntas-list"),
    path("secciones/<int:seccion_id>/preguntas/nueva/", PreguntaCreateView.as_view(), name="preguntas-create"),
    path("preguntas/<int:pk>/editar/", PreguntaUpdateView.as_view(), name="preguntas-update"),
    path("preguntas/<int:pk>/borrar/", PreguntaDeleteView.as_view(), name="preguntas-delete"),

    # CLIENTES
    path("clientes/", ClienteListView.as_view(), name="clientes-list"),
    path("clientes/nuevo/", ClienteCreateView.as_view(), name="clientes-create"),
    path("clientes/<int:pk>/editar/", ClienteUpdateView.as_view(), name="clientes-update"),
    path("clientes/<int:pk>/borrar/", ClienteDeleteView.as_view(), name="clientes-delete"),
]
