from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import (
    Cliente, Cuestionario, Seccion, Pregunta, OpcionRespuesta, Portafolio_v2
)

# ========================
# INDEX
# ========================
from django.shortcuts import render

def index(request):
    return render(request, "inventario/index.html")

# ========================
# CLIENTES
# ========================
class ClienteListView(ListView):
    model = Cliente
    template_name = "inventario/clientes/list.html"
    context_object_name = "clientes"

class ClienteCreateView(CreateView):
    model = Cliente
    template_name = "inventario/clientes/form.html"
    fields = ["nombre", "canal", "direccion", "activo"]

    def get_success_url(self):
        return reverse("clientes-list")

class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = "inventario/clientes/form.html"
    fields = ["nombre", "canal", "direccion", "activo"]

    def get_success_url(self):
        return reverse("clientes-list")

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = "inventario/clientes/confirm_delete.html"

    def get_success_url(self):
        return reverse("clientes-list")

# ========================
# CUESTIONARIOS
# ========================
class CuestionarioListView(ListView):
    model = Cuestionario
    template_name = "inventario/cuestionarios/list.html"
    context_object_name = "cuestionarios"

class CuestionarioCreateView(CreateView):
    model = Cuestionario
    template_name = "inventario/cuestionarios/form.html"
    fields = ["nombre", "canal"]

    def get_success_url(self):
        return reverse("cuestionarios-list")

class CuestionarioUpdateView(UpdateView):
    model = Cuestionario
    template_name = "inventario/cuestionarios/form.html"
    fields = ["nombre", "canal"]

    def get_success_url(self):
        return reverse("cuestionarios-list")

class CuestionarioDeleteView(DeleteView):
    model = Cuestionario
    template_name = "inventario/cuestionarios/confirm_delete.html"

    def get_success_url(self):
        return reverse("cuestionarios-list")

# ========================
# SECCIONES
# ========================
class SeccionListView(ListView):
    model = Seccion
    template_name = "inventario/secciones/list.html"
    context_object_name = "secciones"

    def get_queryset(self):
        self.cuestionario = get_object_or_404(Cuestionario, pk=self.kwargs["cuestionario_id"])
        return Seccion.objects.filter(cuestionario=self.cuestionario).order_by("orden")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cuestionario"] = self.cuestionario
        return ctx

class SeccionCreateView(CreateView):
    model = Seccion
    template_name = "inventario/secciones/form.html"
    fields = ["nombre", "puntos_maximos", "orden"]

    def form_valid(self, form):
        cuestionario = get_object_or_404(Cuestionario, pk=self.kwargs["cuestionario_id"])
        form.instance.cuestionario = cuestionario
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("secciones-list", kwargs={"cuestionario_id": self.kwargs["cuestionario_id"]})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["cuestionario_id"] = self.kwargs["cuestionario_id"]
        return ctx

class SeccionUpdateView(UpdateView):
    model = Seccion
    template_name = "inventario/secciones/form.html"
    fields = ["nombre", "puntos_maximos", "orden"]

    def get_success_url(self):
        return reverse("secciones-list", kwargs={"cuestionario_id": self.object.cuestionario.id})

class SeccionDeleteView(DeleteView):
    model = Seccion
    template_name = "inventario/secciones/confirm_delete.html"

    def get_success_url(self):
        return reverse("secciones-list", kwargs={"cuestionario_id": self.object.cuestionario.id})

# ========================
# PREGUNTAS
# ========================
class PreguntaListView(ListView):
    model = Pregunta
    template_name = "inventario/preguntas/list.html"
    context_object_name = "preguntas"

    def get_queryset(self):
        self.seccion = get_object_or_404(Seccion, pk=self.kwargs["seccion_id"])
        return Pregunta.objects.filter(seccion=self.seccion).order_by("id")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["seccion"] = self.seccion
        ctx["cuestionario"] = self.seccion.cuestionario
        return ctx

class PreguntaCreateView(CreateView):
    model = Pregunta
    template_name = "inventario/preguntas/form.html"
    fields = ["texto", "puntos_maximos", "tipo", "camara"]

    def form_valid(self, form):
        seccion = get_object_or_404(Seccion, pk=self.kwargs["seccion_id"])
        form.instance.seccion = seccion
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("preguntas-list", kwargs={"seccion_id": self.kwargs["seccion_id"]})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["seccion"] = get_object_or_404(Seccion, pk=self.kwargs["seccion_id"])
        return ctx

class PreguntaUpdateView(UpdateView):
    model = Pregunta
    template_name = "inventario/preguntas/form.html"
    fields = ["texto", "puntos_maximos", "tipo", "camara"]

    def get_success_url(self):
        return reverse("preguntas-list", kwargs={"seccion_id": self.object.seccion.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["seccion"] = self.object.seccion
        return ctx

class PreguntaDeleteView(DeleteView):
    model = Pregunta
    template_name = "inventario/preguntas/confirm_delete.html"

    def get_success_url(self):
        return reverse("preguntas-list", kwargs={"seccion_id": self.object.seccion.id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["seccion"] = self.object.seccion
        return ctx

# ========================
# OPCIONES DE RESPUESTA
# ========================
class OpcionRespuestaListView(ListView):
    model = OpcionRespuesta
    template_name = "inventario/opciones/list.html"
    context_object_name = "opciones"

    def get_queryset(self):
        self.pregunta = get_object_or_404(Pregunta, pk=self.kwargs["pregunta_id"])
        return OpcionRespuesta.objects.filter(pregunta=self.pregunta).order_by("orden")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pregunta"] = self.pregunta
        ctx["seccion"] = self.pregunta.seccion
        ctx["cuestionario"] = self.pregunta.seccion.cuestionario
        return ctx

class OpcionRespuestaCreateView(CreateView):
    model = OpcionRespuesta
    template_name = "inventario/opciones/form.html"
    fields = ["texto", "valor", "orden", "tipo"]

    def form_valid(self, form):
        pregunta = get_object_or_404(Pregunta, pk=self.kwargs["pregunta_id"])
        form.instance.pregunta = pregunta
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("opciones-list", kwargs={"pregunta_id": self.kwargs["pregunta_id"]})

class OpcionRespuestaUpdateView(UpdateView):
    model = OpcionRespuesta
    template_name = "inventario/opciones/form.html"
    fields = ["texto", "valor", "orden", "tipo"]

    def get_success_url(self):
        return reverse("opciones-list", kwargs={"pregunta_id": self.object.pregunta.id})

class OpcionRespuestaDeleteView(DeleteView):
    model = OpcionRespuesta
    template_name = "inventario/opciones/confirm_delete.html"

    def get_success_url(self):
        return reverse("opciones-list", kwargs={"pregunta_id": self.object.pregunta.id})

# ========================
# PORTAFOLIO (crear)
# ========================
class PortafolioCreateView(CreateView):
    model = Portafolio_v2
    template_name = "inventario/portafolio/form.html"
    fields = ["cliente", "cuestionario"]

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.usuario = self.request.user
        form.instance.activo = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("portafolio-responder", kwargs={"pk": self.object.id})
