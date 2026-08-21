from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):

    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
}

    return render(
        request,
        "dispositivos/inicio.html",
        contexto,
)


def dispositivos_zona2(request, zona_id):
    if zona_id != 3:
        return HttpResponse(
        "Zona no encontrada", 
        status=404
    )
    
    return HttpResponse(
        f"Dispositivos de la zona {zona_id}"
    )

def dispositivos_zona(request, zona_id):
    contexto = {
        "zona": zona_id,
        "mensaje": f"Dispositivos de la zona {zona_id}",
        "sistema": "EcoEnergy",
    }

    if zona_id != 3:
        contexto = {
            "zona": zona_id,
            "mensaje": "Zona no encontrada",
            "sistema": "EcoEnergy",
        }
    

    return render(
        request,
        "dispositivos/dispositivos_zona.html", 
        contexto,
    )


def catalogo(request):
    dispositivos = [
      {"nombre": "Medidor inteligente", "estado": "Activo"},
      {"nombre": "Sensor de temperatura", "estado": "Activo"},
      {"nombre": "Climatizador", "estado": "Revisión"},
    ]
    return render(
        request,
        "dispositivos/catalogo.html",
        {"dispositivos": dispositivos},
)

