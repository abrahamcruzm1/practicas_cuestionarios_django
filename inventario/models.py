from django.db import models
from django.contrib.auth.models import User

# -----------------------
# CLIENTES
# -----------------------

def canales():
    return [
        ('02 Canal Tradicional', '02 Canal Tradicional'),
        ('05 Canal Mayorista', '05 Canal Mayorista'),
    ]


class Cliente(models.Model):
    # Catálogo de clientes: minisúpers, tiendas grandes o mayoristas
    nombre = models.CharField(max_length=100, unique=True)
    canal = models.CharField(max_length=30, choices=canales(), default='02 Canal Tradicional')
    direccion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        app_label = 'inventario'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} ({self.canal})"


# -----------------------
# CUESTIONARIOS
# -----------------------

class Cuestionario(models.Model):
    # Un cuestionario completo que se aplicará a los clientes
    nombre = models.CharField(max_length=255, default="Cuestionario")
    canal = models.CharField(max_length=30, choices=canales(), default="02 Canal Tradicional")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventario'
        verbose_name = "Cuestionario"
        verbose_name_plural = "Cuestionarios"

    def __str__(self):
        return self.nombre


class Seccion(models.Model):
    # Bloques dentro del cuestionario (ej: Uso de refrigerador, Promociones)
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE, related_name="secciones")
    nombre = models.CharField(max_length=255, blank=True, null=True)
    puntos_maximos = models.IntegerField(default=0)
    orden = models.IntegerField(default=0)

    class Meta:
        app_label = 'inventario'
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"

    def __str__(self):
        return f"{self.nombre} ({self.cuestionario.nombre})"


class Pregunta(models.Model):
    # Pregunta específica dentro de una sección del cuestionario
    TIPO_CAMARA = (
        (0, 'Sin cámara'),
        (1, 'Sí (si responde Sí)'),
        (2, 'No (si responde No)'),
        (3, 'N/D (si responde No Aplica)'),
        (4, 'Siempre requiere foto'),
        (5, 'Sí o N/D'),
    )
    TIPO_PREGUNTA = (
        ('Breve', 'Sí / No'),
        ('Breve1', 'Sí / No / N/D'),
    )

    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name="preguntas")
    texto = models.TextField()  # Texto de la pregunta
    puntos_maximos = models.IntegerField(default=0)
    tipo = models.CharField(max_length=20, choices=TIPO_PREGUNTA, default='Breve')
    camara = models.IntegerField(default=0, choices=TIPO_CAMARA)

    class Meta:
        app_label = 'inventario'
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return self.texto


class OpcionRespuesta(models.Model):
    # Tipos de input HTML que puede tener la opción
    TIPO = (
        ('select', 'Select'),
        ('radio', 'Radio'),
        ('checkbox', 'Checkbox'),
    )

    # Relación con la pregunta a la que pertenece
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="opciones")

    # Texto visible de la opción (ej: "Sí", "No", "N/D")
    texto = models.CharField(max_length=255, blank=True, null=True)

    # Puntaje asociado a la opción
    valor = models.IntegerField(default=0)

    # Orden de aparición en la lista de opciones
    orden = models.IntegerField(default=0)

    # Tipo de input: select, radio o checkbox
    tipo = models.CharField(max_length=20, choices=TIPO, default='radio')

    class Meta:
        app_label = 'inventario'
        verbose_name = "Opción de Respuesta"
        verbose_name_plural = "Opciones de Respuesta"

    def __str__(self):
        return f"{self.texto} ({self.pregunta.texto})"


# -----------------------
# AUDITORÍAS Y RESPUESTAS
# -----------------------

class Portafolio_v2(models.Model):
    # Una auditoría completa hecha a un cliente en un cuestionario
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="portafolios")
    cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE, related_name="portafolios")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="portafolios")
    puntos_obtenidos = models.IntegerField(default=0)
    puntos_maximos = models.IntegerField(default=0)
    porcentaje_ejecucion = models.FloatField(default=0.0)
    porcentaje_contestado = models.FloatField(default=0.0)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        app_label = 'inventario'
        verbose_name = "Portafolio (Auditoría)"
        verbose_name_plural = "Portafolios (Auditorías)"

    def __str__(self):
        return f"Auditoría {self.cuestionario.nombre} - {self.cliente.nombre}"


class PortafolioSeccion(models.Model):
    # Resultados obtenidos por sección dentro de una auditoría
    portafolio = models.ForeignKey(Portafolio_v2, on_delete=models.CASCADE, related_name="secciones")
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name="resultados")
    puntos_obtenidos = models.IntegerField(default=0)
    porcentaje_ejecucion = models.FloatField(default=0.0)
    porcentaje_contestado = models.FloatField(default=0.0)

    class Meta:
        app_label = 'inventario'
        verbose_name = "Resultado por Sección"
        verbose_name_plural = "Resultados por Sección"

    def __str__(self):
        return f"{self.seccion.nombre} - {self.portafolio.cliente.nombre}"


class Respuesta(models.Model):
    portafolio = models.ForeignKey(Portafolio_v2, on_delete=models.CASCADE, related_name="respuestas")
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name="respuestas")
    opcion_respuesta = models.ForeignKey(OpcionRespuesta, on_delete=models.SET_NULL, null=True, blank=True, related_name="respuestas")
    valor = models.IntegerField(default=0)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="respuestas")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        app_label = 'inventario'
        verbose_name = "Respuesta"
        verbose_name_plural = "Respuestas"

    def __str__(self):
        return f"{self.pregunta.texto} -> {self.opcion_respuesta.texto if self.opcion_respuesta else 'Sin respuesta'}"


class Imagen_Respuesta(models.Model):
    # Evidencia fotográfica asociada a una respuesta
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="evidencias/", null=True, blank=True)
    fecha_ejecucion = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="imagenes")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'inventario'
        verbose_name = "Imagen de Respuesta"
        verbose_name_plural = "Imágenes de Respuesta"

    def __str__(self):
        return f"Evidencia de {self.respuesta}"
