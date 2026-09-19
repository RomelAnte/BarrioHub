import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get("ADMIN_USERNAME", "admin")
password = os.environ.get("ADMIN_PASSWORD")
email = os.environ.get("ADMIN_EMAIL", "admin@barriohub.com")

if not password:
    print("[INFO] ADMIN_PASSWORD no especificada en variables de entorno. Omitiendo creación automática de superusuario.")
else:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email=email)
        print(f"[OK] Usuario de administración creado para: {username}")
    else:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"[OK] Contraseña actualizada para usuario: {username}")

