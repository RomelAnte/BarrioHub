import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from feria.models import Aporte, BoletoFisico, SolicitudBoleto, BoletoDigital
from django.core.files.base import ContentFile
import io
from PIL import Image, ImageDraw

def create_sample_image():
    img = Image.new('RGB', (400, 400), color=(37, 99, 235))
    d = ImageDraw.Draw(img)
    d.text((50, 180), "COMPROBANTE FERIA 2026", fill=(255, 255, 255))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return ContentFile(buf.getvalue(), name="sample_comprobante.png")

print("Poblando datos de prueba...")

# 1. APORTES
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

# 2. BOLETOS FÍSICOS
for i in range(1, 21):
    num_str = f"F-{i:03d}"
    estado = 'vendido' if i <= 5 else 'disponible'
    comprador = f"Cliente {i}" if estado == 'vendido' else ""
    telefono = f"09900000{i:02d}" if estado == 'vendido' else ""
    BoletoFisico.objects.get_or_create(
        numero=num_str,
        defaults={
            'estado': estado,
            'comprador': comprador,
            'telefono': telefono
        }
    )

# 3. SOLICITUDES Y BOLETOS DIGITALES CON QR
if not SolicitudBoleto.objects.exists():
    # Solicitud 1 Aprobada
    sol1 = SolicitudBoleto.objects.create(
        nombre_comprador="Pedro Picapiedra",
        cedula="1712345678",
        telefono="0991234567",
        email="pedro@ejemplo.com",
        cantidad=2,
        precio_unitario=2.00,
        total=4.00,
        comprobante=create_sample_image(),
        estado="confirmado",
        notas_admin="Transferencia confirmada en Banco Pichincha"
    )

    b1 = BoletoDigital.objects.create(
        codigo_unico="FERIA-2026-000001",
        solicitud=sol1,
        nombre_comprador=sol1.nombre_comprador,
        estado="confirmado"
    )

    b2 = BoletoDigital.objects.create(
        codigo_unico="FERIA-2026-000002",
        solicitud=sol1,
        nombre_comprador=sol1.nombre_comprador,
        estado="confirmado"
    )

    # Solicitud 2 Pendiente
    sol2 = SolicitudBoleto.objects.create(
        nombre_comprador="Vilma Palma",
        cedula="1798765432",
        telefono="0987654321",
        email="vilma@ejemplo.com",
        cantidad=3,
        precio_unitario=2.00,
        total=6.00,
        comprobante=create_sample_image(),
        estado="pendiente"
    )

print("[OK] Datos de prueba creados exitosamente.")
