from django.contrib import admin
from .models import (
    Cliente, Cuestionario, Seccion, Pregunta, OpcionRespuesta,
    Portafolio_v2, PortafolioSeccion, Respuesta, Imagen_Respuesta
)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "canal", "activo")
    search_fields = ("nombre",)
    list_filter = ("canal", "activo")

@admin.register(Cuestionario)
class CuestionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "canal", "creado")
    search_fields = ("nombre",)
    list_filter = ("canal",)

@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "cuestionario", "orden", "puntos_maximos")
    list_filter = ("cuestionario",)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "texto", "seccion", "tipo", "camara", "puntos_maximos")
    list_filter = ("seccion", "tipo", "camara")

@admin.register(OpcionRespuesta)
class OpcionRespuestaAdmin(admin.ModelAdmin):
    list_display = ("id", "texto", "pregunta", "valor", "orden", "tipo")
    list_filter = ("tipo",)

@admin.register(Portafolio_v2)
class PortafolioAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "cuestionario", "usuario", "puntos_obtenidos", "puntos_maximos", "activo", "creado")
    list_filter = ("activo", "cuestionario")

@admin.register(PortafolioSeccion)
class PortafolioSeccionAdmin(admin.ModelAdmin):
    list_display = ("id", "portafolio", "seccion", "puntos_obtenidos", "porcentaje_ejecucion")

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ("id", "portafolio", "pregunta", "opcion_respuesta", "valor", "usuario", "activo")
    list_filter = ("activo",)

@admin.register(Imagen_Respuesta)
class ImagenRespuestaAdmin(admin.ModelAdmin):
    list_display = ("id", "respuesta", "imagen", "fecha_ejecucion", "activo")
