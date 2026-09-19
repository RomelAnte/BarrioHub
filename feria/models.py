import io
import qrcode
from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone

class Aporte(models.Model):
    BARRIO_CHOICES = [
        ('San Luis', 'San Luis'),
        ('Vista Hermosa', 'Vista Hermosa'),
        ('Quito Occidental', 'Quito Occidental'),
    ]

    CATEGORIA_CHOICES = [
        ('Emprendimiento', 'Emprendimiento'),
        ('Artista', 'Artista'),
        ('Danza', 'Danza'),
        ('Juegos Tradicionales', 'Juegos Tradicionales'),
        ('Otra Propuesta', 'Otra Propuesta'),
    ]

    barrio = models.CharField(max_length=100, choices=BARRIO_CHOICES, verbose_name="Barrio")
    categoria = models.CharField(max_length=100, choices=CATEGORIA_CHOICES, verbose_name="Categoría")
    nombre_aporte = models.CharField(max_length=200, verbose_name="Nombre del Aporte / Emprendimiento")
    responsable = models.CharField(max_length=150, verbose_name="Persona Responsable")
    contacto = models.CharField(max_length=100, verbose_name="Teléfono / Contacto")
    descripcion = models.TextField(blank=True, verbose_name="Descripción u Observaciones")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Aporte"
        verbose_name_plural = "Aportes"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.nombre_aporte} ({self.barrio} - {self.categoria})"


class BoletoFisico(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('vendido', 'Vendido'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Número / Identificador de Boleto")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado")
    comprador = models.CharField(max_length=150, blank=True, verbose_name="Comprador")
    telefono = models.CharField(max_length=50, blank=True, verbose_name="Teléfono Comprador")
    fecha_venta = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Venta")
    notas = models.TextField(blank=True, verbose_name="Notas u Observaciones")

    class Meta:
        verbose_name = "Boleto Físico"
        verbose_name_plural = "Boletos Físicos"
        ordering = ['numero']

    def __str__(self):
        return f"Boleto Físico #{self.numero} - {self.get_estado_display()}"


class SolicitudBoleto(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'En Revisión (Comprobante Subido)'),
        ('confirmado', 'Aprobado / Confirmado'),
        ('rechazado', 'Rechazado'),
    ]

    nombre_comprador = models.CharField(max_length=150, verbose_name="Nombre Completo")
    cedula = models.CharField(max_length=20, verbose_name="Cédula / Identificación")
    telefono = models.CharField(max_length=50, verbose_name="Teléfono WhatsApp")
    email = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad de Boletos")
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2, default=3.00, verbose_name="Precio Unitario ($)")
    total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Total ($)")
    comprobante = models.ImageField(upload_to='comprobantes/', verbose_name="Comprobante de Pago")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")
    notas_admin = models.TextField(blank=True, verbose_name="Notas del Administrador")
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    fecha_respuesta = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Respuesta")

    class Meta:
        verbose_name = "Solicitud de Boleto Digital"
        verbose_name_plural = "Solicitudes de Boletos Digitales"
        ordering = ['-fecha_solicitud']

    def save(self, *args, **kwargs):
        if not self.total and self.cantidad and self.precio_unitario:
            self.total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def get_whatsapp_link(self, request=None):
        import urllib.parse
        phone_digits = ''.join(filter(str.isdigit, self.telefono))
        if phone_digits.startswith('0'):
            phone_digits = '593' + phone_digits[1:]
        elif not phone_digits.startswith('593') and len(phone_digits) == 9:
            phone_digits = '593' + phone_digits

        if request:
            url_detalle = request.build_absolute_uri(f"/preventa/{self.pk}/detalle/")
        else:
            url_detalle = f"/preventa/{self.pk}/detalle/"

        mensaje = (
            f"¡Hola {self.nombre_comprador}! 👋🏼\n\n"
            f"Tu pago para la Feria ha sido *APROBADO* exitosamente. 🎉\n\n"
            f"🎟️ *Detalle de tu compra:*\n"
            f"• Solicitud #{self.id}\n"
            f"• Boletos: {self.cantidad}\n"
            f"• Total: ${self.total} USD\n\n"
            f"📲 *Accede a tus boletos digitales con Código QR aquí:*\n"
            f"{url_detalle}\n\n"
            f"¡Presenta el código QR en la entrada el día de la feria! 🎪"
        )

        return f"https://api.whatsapp.com/send?phone={phone_digits}&text={urllib.parse.quote(mensaje)}"

    def __str__(self):
        return f"Solicitud #{self.id} - {self.nombre_comprador} ({self.cantidad} boletos)"


class BoletoDigital(models.Model):
    ESTADO_CHOICES = [
        ('confirmado', 'VÁLIDO'),
        ('utilizado', 'UTILIZADO'),
        ('cancelado', 'CANCELADO'),
    ]

    codigo_unico = models.CharField(max_length=50, unique=True, verbose_name="Código Único (QR)")
    solicitud = models.ForeignKey(SolicitudBoleto, on_delete=models.CASCADE, related_name='boletos_digitales', verbose_name="Solicitud de Origen")
    nombre_comprador = models.CharField(max_length=150, verbose_name="Nombre Comprador")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='confirmado', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_uso = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Uso en Puerta")
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True, verbose_name="Imagen QR")

    class Meta:
        verbose_name = "Boleto Digital"
        verbose_name_plural = "Boletos Digitales"
        ordering = ['-fecha_creacion']

    def generate_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self.codigo_unico)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        filename = f"qr_{self.codigo_unico}.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Boleto {self.codigo_unico} - {self.nombre_comprador} ({self.get_estado_display()})"
