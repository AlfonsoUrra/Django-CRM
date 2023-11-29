from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Cliente, Proveedor, Producto, PedidoCliente, PedidoProveedor, Stock
from django.core.validators import MaxValueValidator, MinValueValidator


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label = "", widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Email Address'}))
    first_name = forms.CharField(label = "", max_length = 100, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First Name'}))
    last_name = forms.CharField(label = "", max_length = 100, widget = forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last Name'}))

    class Meta:
        model = User
        fields = ('username' , 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	


class AddRecordForm(forms.ModelForm):
    nombre = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Nombre', "class": 'form-control'}), label='')
    empresa = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Empresa', "class": 'form-control'}), label='')
    pais = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'País', "class": 'form-control'}), label='')
    telefono = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Teléfono', "class": 'form-control'}), label='')
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email', "class": 'form-control'}), label='')
    direccion = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Dirección  ', "class": 'form-control'}), label='')
    sector = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Sector', "class": 'form-control'}), label='')

    class Meta:
        model = Cliente
        exclude = ['user',]


class AddSupplierForm(forms.ModelForm):
    nombre = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Nombre', "class": 'form-control'}), label='')
    pais = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'País', "class": 'form-control'}), label='')
    telefono = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Teléfono', "class": 'form-control'}), label='')
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email', "class": 'form-control'}), label='')
    direccion = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Dirección', "class": 'form-control'}), label='')
    eurohoja = forms.BooleanField(
        required=False,
        widget=forms.widgets.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Eurohoja',
    )    
    otras_certificaciones = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={'placeholder': 'Otras Certificaciones', "class": 'form-control'}), label='Otras Certificaciones')


    class Meta:
        model = Proveedor
        exclude = ['user',]  # Si necesitas excluir más campos, añádelos aquí


class AddProductForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), widget=forms.widgets.Select(attrs={'class': 'form-control'}), label='Proveedor')
    pais = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'País', "class": 'form-control'}), label='')
    tipo = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Tipo', "class": 'form-control'}), label='')
    producto = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Producto', "class": 'form-control'}), label='')
    ecologico = forms.BooleanField(required=False, widget=forms.widgets.CheckboxInput(attrs={'class': 'form-check-input'}), label='Ecológico')
    certificaciones = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'placeholder': 'Certificaciones', "class": 'form-control'}), label='Certificaciones')
    pedido_minimo_kg = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Pedido Mínimo (kg)', "class": 'form-control'}), label='Pedido Mínimo (kg)')
    precio_min = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Precio Mínimo', "class": 'form-control'}), label='Precio Mínimo')
    precio_500_kg = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Precio 500 kg', "class": 'form-control'}), label='Precio 500 kg')
    precio_1000_kg = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Precio 1000 kg', "class": 'form-control'}), label='Precio 1000 kg')
    ficha_tecnica = forms.FileField(required=False, widget=forms.widgets.ClearableFileInput(attrs={'class': 'form-control-file'}), label='Ficha Técnica')

    class Meta:
        model = Producto
        exclude = ['user',]


class AddPedidoClienteForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), widget=forms.widgets.Select(attrs={'class': 'form-control'}), label='Proveedor')
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), widget=forms.widgets.Select(attrs={'class': 'form-control'}), label='Producto')
    empresa = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=forms.widgets.Select(attrs={'class': 'form-control'}), label='Empresa')
    cantidad = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Cantidad', 'class': 'form-control'}), label='Cantidad')


    class Meta:
        model = PedidoCliente
        exclude = ['user','precio_final_kg', 'precio_final','gasto_almacen', 'gasto_distribucion', 'precio_total_iva']


class AddPedidoProveedorForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.all(), widget=forms.widgets.Select(attrs={'class': 'form-control'}), label='Proveedor')
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), widget=forms.widgets.Select(attrs={'class': 'form-control'}), label='Producto')
    tipo = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Tipo', 'class': 'form-control'}), label='Tipo')
    nombre = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}), label='Nombre')
    formato = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Formato', 'class': 'form-control'}), label='Formato')
    cantidad = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Cantidad', 'class': 'form-control'}), label='Cantidad')
    precio = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Precio', 'class': 'form-control'}), label='Precio')
    fecha_pedido = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Fecha de Pedido')
    fecha_entrega_prevista = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Fecha de Entrega Prevista')
    

    class Meta:
        model = PedidoProveedor
        exclude = ['user',]


class AddStockForm(forms.ModelForm):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), widget=forms.widgets.Select(attrs={'class': 'form-control'}), label='Producto')
    cantidad = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Cantidad', 'class': 'form-control'}), label='Cantidad')
    formato = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Formato', 'class': 'form-control'}), label='Formato')
    fecha_llegada_prevista = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Fecha de Llegada prevista')
    fecha_llegada_final = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Fecha de Llegada Final')
    precio_proveedor = forms.DecimalField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Precio Proveedor', 'class': 'form-control'}), label='Precio Proveedor')

    class Meta:
        model = Stock
        exclude = ['user',]


