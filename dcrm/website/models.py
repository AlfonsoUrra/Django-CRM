from django.db import models
from django.utils import timezone

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField()
    eurohoja = models.BooleanField(default=False)
    otras_certificaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.id}: {self.nombre}"

class Producto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    precio_por_kg = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id}: {self.nombre} ({self.proveedor})"

class DetallePedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2)
    costo_proveedor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_almacenamiento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def calcular_costo_detalle(self):
        costo_base = self.cantidad_kg * self.producto.precio_por_kg  # Costo basado en la cantidad y el precio por kg del producto

    def save(self, *args, **kwargs):
        self.costo_proveedor = self.producto.precio_por_kg * self.cantidad_kg
        self.costo_almacenamiento = self.calcular_costo_detalle()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: {self.producto} - {self.cantidad_kg} kg"

class Almacen(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    gdp = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id}: {self.nombre}"

class Zona(models.Model):
    nombre = models.CharField(max_length=255)
    numero = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.nombre}"

class CosteEnvio(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    peso_hasta = models.IntegerField()
    plazo_24h = models.DecimalField(max_digits=10, decimal_places=2)
    plazo_48_72h = models.DecimalField(max_digits=10, decimal_places=2)
    costo_por_kilo = models.DecimalField(max_digits=10, decimal_places=2)  # Nuevo campo

    def __str__(self):
        return f"{self.id}: {self.zona} - Hasta {self.peso_hasta} Kg - 24h: {self.plazo_24h}, 48-72h: {self.plazo_48_72h}, Costo/Kg: {self.costo_por_kilo}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField()
    sector = models.CharField(max_length=255)
    creado = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.id}: {self.nombre}"

class Pedido(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    detalles_pedido = models.ManyToManyField(DetallePedido)
    costo_proveedor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_almacenamiento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plazo_envio = models.CharField(max_length=10)  # Puedes ajustar la longitud según tus necesidades

    def calcular_costo_almacenamiento(self):
        return sum(detalle.costo_almacenamiento for detalle in self.detalles_pedido.all())

    def calcular_costo_envio(self):
        costo_total_envio = 0
        for detalle in self.detalles_pedido.all():
            costo_envio = CosteEnvio.objects.filter(zona__numero=detalle.producto.zona.numero, peso_hasta__gte=detalle.cantidad_kg).first()
            costo_total_envio += detalle.cantidad_kg * costo_envio.costo_por_kilo
            if detalle.cantidad_kg <= 1000:
                costo_total_envio += costo_envio.plazo_24h
            else:
                costo_total_envio += costo_envio.plazo_48_72h
        return costo_total_envio

    def calcular_costo_total(self):
        return self.calcular_costo_proveedor() + self.calcular_costo_almacenamiento() + self.calcular_costo_envio()
