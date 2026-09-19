import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .models import Aporte, SolicitudBoleto, BoletoDigital
from .forms import AporteForm, SolicitudBoletoForm


def index(request):
    """Página de inicio con resumen del evento y accesos rápidos"""
    stats = {
        'total_aportes': Aporte.objects.count(),
        'emprendimientos': Aporte.objects.filter(categoria='Emprendimiento').count(),
        'solicitudes_pendientes': SolicitudBoleto.objects.filter(estado='pendiente').count(),
        'boletos_digitales_validos': BoletoDigital.objects.filter(estado='confirmado').count(),
        'boletos_digitales_utilizados': BoletoDigital.objects.filter(estado='utilizado').count(),
    }
    return render(request, 'feria/index.html', {'stats': stats})


# ==========================================
# AUTENTICACIÓN SIMPLE
# ==========================================

def login_view(request):
    """Inicio de sesión simple para el comité organizador"""
    if request.user.is_authenticated:
        return redirect('admin_boletos')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}! Has ingresado al panel de administración.')
            next_url = request.GET.get('next', 'admin_boletos')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'feria/login.html', {'form': form})


def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('index')


# ==========================================
# 1. MÓDULO APORTES DE LOS 3 BARRIOS (PÚBLICO)
# ==========================================

def aportes_list(request):
    """Pantalla para consultar, buscar y filtrar todos los aportes de los 3 barrios"""
    query = request.GET.get('q', '').strip()
    barrio_filter = request.GET.get('barrio', '').strip()
    categoria_filter = request.GET.get('categoria', '').strip()

    aportes = Aporte.objects.all()

    if query:
        aportes = aportes.filter(
            Q(nombre_aporte__icontains=query) |
            Q(responsable__icontains=query) |
            Q(contacto__icontains=query) |
            Q(descripcion__icontains=query)
        )

    if barrio_filter:
        aportes = aportes.filter(barrio=barrio_filter)

    if categoria_filter:
        aportes = aportes.filter(categoria=categoria_filter)

    barrios = Aporte.BARRIO_CHOICES
    categorias = [c[0] for c in Aporte.CATEGORIA_CHOICES]

    context = {
        'aportes': aportes,
        'query': query,
        'barrio_filter': barrio_filter,
        'categoria_filter': categoria_filter,
        'barrios': barrios,
        'categorias': categorias,
        'total_resultados': aportes.count()
    }
    return render(request, 'feria/aportes_list.html', context)


def aporte_create(request):
    """Registrar un nuevo aporte"""
    if request.method == 'POST':
        form = AporteForm(request.POST)
        if form.is_valid():
            aporte = form.save()
            messages.success(request, f'¡Aporte "{aporte.nombre_aporte}" registrado correctamente para el {aporte.barrio}!')
            return redirect('aportes_list')
    else:
        form = AporteForm()
    return render(request, 'feria/aporte_form.html', {'form': form, 'title': 'Registrar Nuevo Aporte'})


@login_required(login_url='login')
def aporte_edit(request, pk):
    """Editar un aporte existente (Protegido)"""
    aporte = get_object_or_404(Aporte, pk=pk)
    if request.method == 'POST':
        form = AporteForm(request.POST, instance=aporte)
        if form.is_valid():
            form.save()
            messages.success(request, f'Aporte "{aporte.nombre_aporte}" actualizado con éxito.')
            return redirect('aportes_list')
    else:
        form = AporteForm(instance=aporte)
    return render(request, 'feria/aporte_form.html', {'form': form, 'title': 'Editar Aporte', 'aporte': aporte})


@login_required(login_url='login')
def aporte_delete(request, pk):
    """Eliminar un aporte (Protegido)"""
    aporte = get_object_or_404(Aporte, pk=pk)
    if request.method == 'POST':
        nombre = aporte.nombre_aporte
        aporte.delete()
        messages.warning(request, f'Aporte "{nombre}" eliminado.')
        return redirect('aportes_list')
    return render(request, 'feria/aporte_confirm_delete.html', {'aporte': aporte})





# ==========================================
# 3. PREVENTA DE BOLETOS DIGITALES (PÚBLICO)
# ==========================================

def solicitud_digital(request):
    """Formulario público para solicitar boletos digitales y subir comprobante"""
    if request.method == 'POST':
        form = SolicitudBoletoForm(request.POST, request.FILES)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.precio_unitario = 3.00  # Precio base de boleto preventa
            solicitud.total = solicitud.cantidad * solicitud.precio_unitario
            solicitud.estado = 'pendiente'
            solicitud.save()
            messages.success(request, '¡Tu solicitud y comprobante fueron enviados con éxito! El comité lo revisará en breve.')
            return redirect('solicitud_confirmacion', pk=solicitud.pk)
    else:
        form = SolicitudBoletoForm()
    
    # Datos de transferencia bancaria para el usuario
    datos_banco = {
        'banco': 'Banco Pichincha',
        'tipo_cuenta': 'Cuenta de Ahorros',
        'numero_cuenta': '2209876543',
        'titular': 'Comité Feria de Seguridad',
        'identificacion': '1798765432001',
        'email': 'feriaseguridad.barrios@gmail.com',
        'precio_unitario': 3.00
    }
    return render(request, 'feria/solicitud_digital.html', {'form': form, 'datos_banco': datos_banco})


def solicitud_confirmacion(request, pk):
    """Pantalla de confirmación tras registrar solicitud digital"""
    solicitud = get_object_or_404(SolicitudBoleto, pk=pk)
    return render(request, 'feria/solicitud_confirmacion.html', {'solicitud': solicitud})


def solicitud_detalle_publico(request, pk):
    """Ver estado público de la solicitud y descargar boletos si fue aprobada"""
    solicitud = get_object_or_404(SolicitudBoleto, pk=pk)
    boletos = solicitud.boletos_digitales.all()
    return render(request, 'feria/solicitud_detalle_publico.html', {'solicitud': solicitud, 'boletos': boletos})


# ==========================================
# 4. ADMINISTRACIÓN DE BOLETOS Y REVISIÓN (PROTEGIDO)
# ==========================================

@login_required(login_url='login')
def admin_boletos(request):
    """Pantalla de administración para revisar comprobantes y aprobar/rechazar solicitudes"""
    query = request.GET.get('q', '').strip()
    estado_filter = request.GET.get('estado', '').strip()

    solicitudes = SolicitudBoleto.objects.all()

    if query:
        solicitudes = solicitudes.filter(
            Q(nombre_comprador__icontains=query) |
            Q(cedula__icontains=query) |
            Q(telefono__icontains=query)
        )

    if estado_filter:
        solicitudes = solicitudes.filter(estado=estado_filter)

    boletos_digitales = BoletoDigital.objects.all()
    if query:
        boletos_digitales = boletos_digitales.filter(
            Q(codigo_unico__icontains=query) |
            Q(nombre_comprador__icontains=query)
        )

    for sol in solicitudes:
        sol.wa_link = sol.get_whatsapp_link(request)

    context = {
        'solicitudes': solicitudes,
        'boletos_digitales': boletos_digitales,
        'query': query,
        'estado_filter': estado_filter,
        'pendientes_count': SolicitudBoleto.objects.filter(estado='pendiente').count(),
    }
    return render(request, 'feria/admin_boletos.html', context)


@login_required(login_url='login')
def aprobar_solicitud(request, pk):
    """Aprobar solicitud digital y generar automáticamente los boletos digitales con código QR único"""
    solicitud = get_object_or_404(SolicitudBoleto, pk=pk)
    
    if request.method == 'POST':
        if solicitud.estado != 'confirmado':
            solicitud.estado = 'confirmado'
            solicitud.fecha_respuesta = timezone.now()
            solicitud.notas_admin = request.POST.get('notas_admin', '').strip()
            solicitud.save()

            # Generar N boletos digitales según la cantidad solicitada
            for i in range(solicitud.cantidad):
                consecutivo = BoletoDigital.objects.count() + 1
                codigo = f"FERIA-2026-{consecutivo:06d}"
                
                while BoletoDigital.objects.filter(codigo_unico=codigo).exists():
                    consecutivo += 1
                    codigo = f"FERIA-2026-{consecutivo:06d}"

                BoletoDigital.objects.create(
                    codigo_unico=codigo,
                    solicitud=solicitud,
                    nombre_comprador=solicitud.nombre_comprador,
                    estado='confirmado'
                )

            messages.success(request, f'¡Solicitud #{solicitud.id} APROBADA! Se generaron {solicitud.cantidad} boletos digitales con código QR.')
        else:
            messages.info(request, 'Esta solicitud ya había sido aprobada previamente.')
            
    return redirect('admin_boletos')


@login_required(login_url='login')
def rechazar_solicitud(request, pk):
    """Rechazar solicitud digital"""
    solicitud = get_object_or_404(SolicitudBoleto, pk=pk)
    if request.method == 'POST':
        solicitud.estado = 'rechazado'
        solicitud.fecha_respuesta = timezone.now()
        solicitud.notas_admin = request.POST.get('notas_admin', 'Comprobante no válido o ilegible.').strip()
        solicitud.save()
        messages.warning(request, f'Solicitud #{solicitud.id} fue RECHAZADA.')
    return redirect('admin_boletos')


# ==========================================
# 5. ESCÁNER Y VALIDACIÓN DE BOLETO CON QR (PROTEGIDO)
# ==========================================

@login_required(login_url='login')
def validar_qr(request):
    """Pantalla para consultar y validar boletos en puerta"""
    codigo = request.GET.get('codigo', '').strip().upper()
    resultado = None
    boleto = None

    if codigo:
        try:
            boleto = BoletoDigital.objects.get(codigo_unico=codigo)
            if boleto.estado == 'confirmado':
                resultado = 'VALIDO'  # ✅ BOLETO VÁLIDO
            elif boleto.estado == 'utilizado':
                resultado = 'UTILIZADO'  # ⚠️ BOLETO YA UTILIZADO
            else:
                resultado = 'NO_VALIDO'  # ❌ BOLETO CANCELADO/RECHAZADO
        except BoletoDigital.DoesNotExist:
            resultado = 'NO_EXISTE'  # ❌ CÓDIGO NO ENCONTRADO

    return render(request, 'feria/validar_qr.html', {
        'codigo': codigo,
        'resultado': resultado,
        'boleto': boleto
    })


@login_required(login_url='login')
def marcar_boleto_utilizado(request, pk):
    """Marcar un boleto digital confirmado como utilizado inmediatamente"""
    boleto = get_object_or_404(BoletoDigital, pk=pk)
    if request.method == 'POST':
        if boleto.estado == 'confirmado':
            boleto.estado = 'utilizado'
            boleto.fecha_uso = timezone.now()
            boleto.save()
            messages.success(request, f'✅ ¡Boleto {boleto.codigo_unico} de {boleto.nombre_comprador} MARCADO COMO UTILIZADO!')
        elif boleto.estado == 'utilizado':
            messages.warning(request, f'⚠️ Este boleto ya fue utilizado el {boleto.fecha_uso.strftime("%d/%m/%Y %H:%M")}.')
    return redirect(f'/validar/?codigo={boleto.codigo_unico}')
