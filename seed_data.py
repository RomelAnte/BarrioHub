import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from feria.models import Aporte, SolicitudBoleto, BoletoDigital, BoletoFisico
from django.db import connection

print("Iniciando verificación y mantenimiento de datos...")

# 1. APORTES BASE DE EJEMPLO
aportes_data = [
    {
        'barrio': 'San Luis',
        'categoria': 'Emprendimiento',
        'nombre_aporte': 'Hornado Tradicional La Delicia',
        'responsable': 'Carlos Andrade',
        'contacto': '0998765432',
        'descripcion': 'Stand de comida típica ecuatoriana con hornado, mote y tostado.'
    },
    {
        'barrio': 'San Luis',
        'categoria': 'Danza',
        'nombre_aporte': 'Grupo Folklorico Raíces del Sur',
        'responsable': 'María Fernanda López',
        'contacto': '0981234567',
        'descripcion': 'Presentación de 12 bailarines con trajes típicos andinos.'
    },
    {
        'barrio': 'Vista Hermosa',
        'categoria': 'Emprendimiento',
        'nombre_aporte': 'Artesanías y Manualidades en Madera',
        'responsable': 'Jorge Benítez',
        'contacto': '0995554433',
        'descripcion': 'Venta de adornos para el hogar y juguetes de madera tallada.'
    },
    {
        'barrio': 'Vista Hermosa',
        'categoria': 'Artista',
        'nombre_aporte': 'Trío Musical Los Caminantes',
        'responsable': 'Gonzalo Ramírez',
        'contacto': '0976543210',
        'descripcion': 'Música en vivo con guitarras y pasillos ecuatorianos.'
    },
    {
        'barrio': 'Quito Occidental',
        'categoria': 'Juegos Tradicionales',
        'nombre_aporte': 'Carrera de Ensacados y Trompos',
        'responsable': 'Lucía Morales',
        'contacto': '0991112233',
        'descripcion': 'Juegos recreativos con premios para niños y familias.'
    },
    {
        'barrio': 'Quito Occidental',
        'categoria': 'Emprendimiento',
        'nombre_aporte': 'Helados de Paila Artesanales',
        'responsable': 'Ana Lucía Torres',
        'contacto': '0989998877',
        'descripcion': 'Helados artesanales de mora, guanábana y maracuyá.'
    }
]

for item in aportes_data:
    Aporte.objects.get_or_create(
        nombre_aporte=item['nombre_aporte'],
        defaults=item
    )

def reset_tickets_and_ids():
    """Elimina solicitudes/boletos de prueba y reinicia los contadores de secuencia de SQLite a 1"""
    BoletoDigital.objects.all().delete()
    SolicitudBoleto.objects.all().delete()
    BoletoFisico.objects.all().delete()
    
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('feria_solicitudboleto', 'feria_boletodigital', 'feria_boletofisico');")
    
    print("[OK] Se han limpiado las solicitudes y reiniciado la secuencia de IDs a 1.")

if __name__ == '__main__':
    reset_tickets_and_ids()
