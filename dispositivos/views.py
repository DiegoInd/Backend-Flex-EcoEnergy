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


# -------------------------------------------------------------------
# FASE 2: Nueva función agregada
# -------------------------------------------------------------------
def resumen_zonas(request):
    zonas_data = cargar_json('zonas.json')
    dispositivos_data = cargar_json('dispositivos.json')

    # Agrupar dispositivos por zona_id
    dispositivos_por_zona = {}
    for dev in dispositivos_data:
        z_id = dev.get('zona_id') or dev.get('id_zona')
        if z_id not in dispositivos_por_zona:
            dispositivos_por_zona[z_id] = []
        dispositivos_por_zona[z_id].append(dev)

    resumen_list = []
    consumo_total_global = 0.0

    for zona in zonas_data:
        z_id = zona.get('id')
        nombre = zona.get('nombre', 'Sin Nombre')
        limite_kwh = float(zona.get('limite_kwh', 0.0))

        devs_asociados = dispositivos_por_zona.get(z_id, [])
        cant_dispositivos = len(devs_asociados)
        consumo_total = sum(float(d.get('consumo_kwh', 0.0)) for d in devs_asociados)

        consumo_total_global += consumo_total

        # Regla de negocio de la Fase 2
        if consumo_total <= limite_kwh:
            estado_texto = "DENTRO DEL LÍMITE"
            estado_badge_class = "bg-success"
            estado_icono = "bi-check-circle-fill"
        else:
            estado_texto = "LÍMITE SUPERADO"
            estado_badge_class = "bg-danger"
            estado_icono = "bi-exclamation-triangle-fill"

        resumen_list.append({
            'id': z_id,
            'nombre': nombre,
            'cantidad_dispositivos': cant_dispositivos,
            'consumo_total': consumo_total,
            'limite_kwh': limite_kwh,
            'estado_texto': estado_texto,
            'estado_badge_class': estado_badge_class,
            'estado_icono': estado_icono,
        })

    context = {
        'total_zonas': len(zonas_data),
        'total_dispositivos': len(dispositivos_data),
        'consumo_total_global': consumo_total_global,
        'resumen_zonas': resumen_list,
    }

    return render(request, 'dispositivos/resumenes-zonas.html', context)