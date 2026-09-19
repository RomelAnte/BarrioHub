# 🏘️ BarrioHub - Sistema de Gestión de Ferias Barriales y Boletaje Digital

**BarrioHub** es una plataforma web integral desarrollada en **Django** para organizar, administrar y dinamizar ferias barriales y eventos comunitarios. Permite la gestión centralizada de emprendimientos/aportes comunitarios, la comercialización de boletos físicos y preventa digital con verificación de pagos mediante comprobante, y la validación en tiempo real en puerta a través de códigos QR.

---

## 📌 Problema

La organización de eventos y ferias en sectores comunitarios o barriales (ej. barrios como *San Luis*, *Vista Hermosa*, *Quito Occidental*) suele enfrentar diversas dificultades logísticas e informales:

- **Descontrol en el boletaje:** Dificultad para coordinar ventas de entradas físicas frente a preventas digitales.
- **Validación manual lenta:** Filas extensas en puerta y riesgo de fraude o duplicación de boletos.
- **Gestión informal de pagos:** Procesamiento manual complejo de transferencias bancarias y comprobantes de preventa.
- **Desarticulación Comunitaria:** Falta de un registro ordenado de emprendedores, artistas, agrupaciones de danza y propuestas de entretenimiento barrial.

---

## 🎯 Objetivo

Proveer una solución tecnológica accesible, robusta y centralizada que automatice el ciclo de vida completo de una feria barrial:

1. **Visibilizar y registrar** los emprendimientos y aportes culturales/gastronómicos/de entretenimiento por barrio.
2. **Facilitar la preventa digital** de boletos mediante carga de comprobantes de pago.
3. **Agilizar la administración** permitiendo validar y aprobar transferencias bancarias para generar boletos con QR único.
4. **Garantizar un control de acceso rápido y seguro** mediante una herramienta de escaneo y validación de QR en puerta.

---

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.10+ & Django 5.x / 6.x
- **Base de Datos:** SQLite3 (Desarrollo) / PostgreSQL (Producción mediante `dj-database-url`)
- **Frontend:** HTML5, CSS3 (Diseño responsivo moderno) y JavaScript (para interfaz interactiva y lectura QR)
- **Generación de QR:** `qrcode` (Pillow)
- **Servidor y Archivos Estáticos:** Gunicorn, WhiteNoise
- **Despliegue / PaaS:** Render (Soporte mediante script `build.sh`)

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue el patrón **MVT (Model-View-Template)** propio de Django, agrupado en la aplicación principal `feria`:

```text
BarrioHub/
├── config/                  # Configuración global del proyecto Django (settings, urls, wsgi)
├── feria/                   # Aplicación principal
│   ├── models.py            # Modelos: Aporte, BoletoFisico, SolicitudBoleto, BoletoDigital
│   ├── views.py             # Lógica de negocio (Autenticación, Aportes, Preventa, Admin, Scanner)
│   ├── forms.py             # Formularios para aportes, solicitudes y administración
│   ├── urls.py              # Enrutamiento de URLs de la feria
│   └── templates/feria/     # Plantillas HTML desglosadas por funcionalidad
├── static/                  # Archivos estáticos (CSS, JS, imágenes)
├── media/                   # Comprobantes subidos y Códigos QR generados
├── build.sh                 # Script de compilación y despliegue automático
├── seed_data.py             # Poblamiento inicial de datos demo
├── create_admin.py          # Creación automatizada del superusuario inicial
├── requirements.txt         # Dependencias del proyecto
└── manage.py                # Script CLI de Django
```

### 🔄 Flujo del Boletaje Digital:
1. **Solicitud de Preventa:** El usuario llena sus datos y adjunta su comprobante de pago en el formulario público `/preventa/`.
2. **Revisión Administrativa:** El administrador revisa el comprobante desde `/admin-boletos/`.
3. **Generación de Boleto:** Al aprobar la solicitud, el sistema genera automáticamente uno o varios `BoletoDigital` con su código único e imagen de **Código QR**.
4. **Validación en Puerta:** El staff de acceso escanea el código QR desde `/validar/`, el sistema verifica su validez y lo marca como `UTILIZADO`.

---

## ⚡ Funcionalidades

### 🛒 1. Módulo de Preventa Digital Pública
- Formulario intuitivo para que los usuarios compren boletos.
- Cálculo automático del monto total según la cantidad de boletos.
- Carga e historial de comprobantes de pago.
- Visualización y descarga del boleto digital con su código QR.

### 🛡️ 2. Panel de Administración de Boletos
- Listado de solicitudes pendientes de verificación.
- Visualización directa del comprobante de pago subido.
- Acciones de aprobación o rechazo en un solo clic.

### 🎟️ 3. Control de Boletos Físicos
- Registro e inventario de boletos físicos impresos.
- Control de estados: *Disponible* vs *Vendido*.
- Registro de datos del comprador y fecha de venta.

### 📲 4. Escáner y Validador de QR en Puerta
- Validador web en tiempo real para verificar la autenticidad del boleto.
- Detección de boletos ya utilizados o cancelados para evitar doble ingreso.
- Cambio inmediato de estado a *UTILIZADO* con registro de fecha y hora.

### 🎪 5. Gestión de Aportes y Emprendimientos Barriales
- Registro de propuestas clasificadas por categoría (*Emprendimiento, Artista, Danza, Juegos Tradicionales, Otra Propuesta*).
- Segmentación por barrio (*San Luis, Vista Hermosa, Quito Occidental*).
- CRUD completo (Crear, Leer, Editar, Eliminar) para los organizadores.

---

## 📊 Estado Actual del Proyecto

- **Estado:** `MVP Funcional / Listo para Producción (Production Ready)`
- **Lógica Core:** 100% Implementada y provista de scripts de seeding de datos para pruebas rápidas (`seed_data.py`).
- **Autenticación:** Sistema de inicio de sesión con roles diferenciados para administración y validación.
- **Despliegue:** Configurado para despliegues continuos en plataformas cloud como Render.

---

## 📷 Capturas de Pantalla

*(Añade tus capturas de pantalla ubicándolas en la carpeta `docs/screenshots/`)*

| Inicio y Registro de Aportes | Preventa Digital de Boletos |
| :---: | :---: |
| ![Inicio](docs/screenshots/inicio.png) | ![Preventa](docs/screenshots/preventa.png) |

| Administración y Aprobación de Pagos | Validador y Escáner QR en Puerta |
| :---: | :---: |
| ![Admin Boletos](docs/screenshots/admin_boletos.png) | ![Validar QR](docs/screenshots/validar_qr.png) |

---

## 🚀 Cómo Ejecutar el Proyecto

### Prerrequisitos
- **Python** 3.10 o superior
- **Git**

### Pasos de Instalación Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/RomelAnte/BarrioHub.git
   cd BarrioHub
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   # En Linux / macOS:
   python3 -m venv venv
   source venv/bin/activate

   # En Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar migraciones y poblar datos demo:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser # O ejecutar create_admin.py con variables de entorno ADMIN_USERNAME y ADMIN_PASSWORD
   python seed_data.py               # Genera aportes y boletos demo
   ```

5. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

6. **Acceder en el navegador:**
   - App Principal: `http://127.0.0.1:8000/`
   - Preventa Digital: `http://127.0.0.1:8000/preventa/`
   - Panel de Control: `http://127.0.0.1:8000/admin-boletos/`
   - Validador QR: `http://127.0.0.1:8000/validar/`

---

## 🗺️ Roadmap / Próximos Pasos

- [ ] **Pasarelas de Pago Automáticas:** Integración con PayPhone / Stripe / PayPal para confirmación inmediata sin revisión manual de comprobante.
- [ ] **Notificaciones Automáticas:** Envío de boletos digitales y confirmaciones directamente a través de **WhatsApp API** (Twilio/Meta) y Correo Electrónico.
- [ ] **Modo Offline PWA para Escáner:** Permite a los validadores en puerta seguir escaneando y validando boletos aun si falla la conexión a internet en el recinto.
- [ ] **Exportación de Reportes:** Generación de reportes financieros, liquidación de taquilla e inventario en formatos PDF y Excel.
- [ ] **Soporte Multi-Evento:** Evolución hacia una plataforma SaaS que administre múltiples ferias y eventos barriales en simultáneo.

---

Elaborado para potenciar la autogestión y dinamización de eventos comunitarios 🚀
