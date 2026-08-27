import json
import os
from django.shortcuts import render
from django.http import Http404
from django.conf import settings

# Ruta a la carpeta data en la raíz del proyecto
DATA_DIR = os.path.join(settings.BASE_DIR, 'data')

def cargar_json(nombre_archivo):
    ruta = os.path.join(DATA_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def listado_zonas(request):
    zonas = cargar_json('zonas.json')
    dispositivos = cargar_json('dispositivos.json')

    # Calcular la cantidad de dispositivos por zona dinámicamente
    for zona in zonas:
        zona['cant_dispositivos'] = sum(1 for d in dispositivos if d.get('zona_id') == zona['id'])

    return render(request, 'dispositivos/listado_zonas.html', {'zonas': zonas})

def detalle_zona(request, zona_id):
    zonas = cargar_json('zonas.json')
    categorias = cargar_json('categorias.json')
    dispositivos = cargar_json('dispositivos.json')

    # Buscar la zona correspondiente
    zona = next((z for z in zonas if z['id'] == zona_id), None)
    if not zona:
        raise Http404("La zona consultada no existe.")

    # Filtrar dispositivos pertenecientes a la zona
    dispositivos_zona = [d for d in dispositivos if d.get('zona_id') == zona_id]

    # Mapear nombres de categorías y calcular consumo total
    cat_dict = {c['id']: c['nombre'] for c in categorias}
    consumo_total = 0.0

    for d in dispositivos_zona:
        d['categoria_nombre'] = cat_dict.get(d.get('categoria_id'), 'Sin Categoría')
        consumo_total += float(d.get('consumo_kwh', 0))

    # Regla CA-05: ALERTA cuando consumo_total > limite_kwh
    estado = "ALERTA" if consumo_total > zona['limite_kwh'] else "NORMAL"

    contexto = {
        'zona': zona,
        'dispositivos': dispositivos_zona,
        'consumo_total': consumo_total,
        'estado': estado,
        'cant_dispositivos': len(dispositivos_zona)
    }

    return render(request, 'dispositivos/detalle_zona.html', contexto)