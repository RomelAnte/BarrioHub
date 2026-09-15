from django.contrib import admin
from .models import Aporte, BoletoFisico, SolicitudBoleto, BoletoDigital

@admin.register(Aporte)
class AporteAdmin(admin.ModelAdmin):
    list_display = ('nombre_aporte', 'barrio', 'categoria', 'responsable', 'contacto', 'fecha_registro')
    list_filter = ('barrio', 'categoria')
    search_fields = ('nombre_aporte', 'responsable', 'contacto', 'descripcion')

@admin.register(BoletoFisico)
class BoletoFisicoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'estado', 'comprador', 'telefono', 'fecha_venta')
    list_filter = ('estado',)
    search_fields = ('numero', 'comprador', 'telefono')

@admin.register(SolicitudBoleto)
class SolicitudBoletoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_comprador', 'cedula', 'cantidad', 'total', 'estado', 'fecha_solicitud')
    list_filter = ('estado',)
    search_fields = ('nombre_comprador', 'cedula', 'telefono')

@admin.register(BoletoDigital)
class BoletoDigitalAdmin(admin.ModelAdmin):
    list_display = ('codigo_unico', 'nombre_comprador', 'estado', 'fecha_creacion', 'fecha_uso')
    list_filter = ('estado',)
    search_fields = ('codigo_unico', 'nombre_comprador')
