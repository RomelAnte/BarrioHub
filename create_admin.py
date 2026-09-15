import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

username = "admin"
password = "feria2026"
email = "admin@feriaseguridad.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f"[OK] Usuario de administracion creado: {username} / {password}")
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"[OK] Contrasena actualizada para usuario: {username} / {password}")
