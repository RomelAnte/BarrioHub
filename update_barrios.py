import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from feria.models import Aporte

# Mapear nombres anteriores a los nuevos barrios
mapping = {
    'Barrio 1': 'San Luis',
    'Barrio 2': 'Vista Hermosa',
    'Barrio 3': 'Quito Occidental',
}

actualizados = 0
for old_name, new_name in mapping.items():
    count = Aporte.objects.filter(barrio=old_name).update(barrio=new_name)
    actualizados += count

print(f"[OK] Se actualizaron {actualizados} registros de aportes con los nuevos nombres de barrio.")
