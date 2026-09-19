from django import forms
from .models import Aporte, SolicitudBoleto

class AporteForm(forms.ModelForm):
    class Meta:
        model = Aporte
        fields = ['barrio', 'categoria', 'nombre_aporte', 'responsable', 'contacto', 'descripcion']
        widgets = {
            'barrio': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'nombre_aporte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Gastronomía Tradicional / Grupo de Danza'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre y Apellido del responsable'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono o WhatsApp de contacto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalles adicionales, insumos o espacio requerido'}),
        }




class SolicitudBoletoForm(forms.ModelForm):
    class Meta:
        model = SolicitudBoleto
        fields = ['nombre_comprador', 'cedula', 'telefono', 'email', 'cantidad', 'comprobante']
        widgets = {
            'nombre_comprador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Juan Pérez'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1712345678'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0991234567'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com (opcional)'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 50, 'value': 1, 'id': 'id_cantidad'}),
            'comprobante': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
