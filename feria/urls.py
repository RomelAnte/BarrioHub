from django.urls import path
from . import views

urlpatterns = [
    # Inicio y Autenticación
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # 1. Aportes
    path('aportes/', views.aportes_list, name='aportes_list'),
    path('aportes/nuevo/', views.aporte_create, name='aporte_create'),
    path('aportes/<int:pk>/editar/', views.aporte_edit, name='aporte_edit'),
    path('aportes/<int:pk>/eliminar/', views.aporte_delete, name='aporte_delete'),


    # 3. Solicitud Digital Pública
    path('preventa/', views.solicitud_digital, name='solicitud_digital'),
    path('preventa/<int:pk>/confirmacion/', views.solicitud_confirmacion, name='solicitud_confirmacion'),
    path('preventa/<int:pk>/detalle/', views.solicitud_detalle_publico, name='solicitud_detalle_publico'),

    # 4. Administración de Boletos
    path('admin-boletos/', views.admin_boletos, name='admin_boletos'),
    path('admin-boletos/<int:pk>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('admin-boletos/<int:pk>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),

    # 5. Escáner y Validación QR
    path('validar/', views.validar_qr, name='validar_qr'),
    path('validar/<int:pk>/usar/', views.marcar_boleto_utilizado, name='marcar_boleto_utilizado'),
]
