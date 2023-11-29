from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField()
    eurohoja = models.BooleanField(default=False)
    otras_certificaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre}"
    

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField()
    sector = models.CharField(max_length=255)
    creado = models.DateTimeField(default=timezone.now)
    
    campo_a_mostrar = None  # Variable de clase para almacenar la elección

    def __str__(self):
        if self.campo_a_mostrar == 'nombre':
            return f"{self.id}: Nombre - {self.nombre}"
        elif self.campo_a_mostrar == 'empresa':
            return f"{self.id}: Empresa - {self.empresa}"
        elif self.campo_a_mostrar == 'email':
            return f"{self.id}: Email - {self.email}"
            
        return f"{self.empresa}"


class Producto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    pais = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    producto = models.CharField(max_length=255)
    ecologico = models.BooleanField(default=False)
    certificaciones = models.TextField()
    pedido_minimo_kg = models.DecimalField(max_digits=10, decimal_places=2)
    precio_min = models.DecimalField(max_digits=10, decimal_places=2)
    precio_500_kg = models.DecimalField(max_digits=10, decimal_places=2)
    precio_1000_kg = models.DecimalField(max_digits=10, decimal_places=2)
    ficha_tecnica = models.FileField(upload_to='fichas_tecnicas/', null=True, blank=True)

    def __str__(self):
        return f" ({self.proveedor} - {self.producto})"
    

class Stock(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    formato = models.CharField(max_length=10)  # Kg, Unidad, etc.
    fecha_llegada_prevista = models.DateField()
    fecha_llegada_final = models.DateField()
    precio_proveedor = models.DecimalField(max_digits=10, decimal_places=2)  # Nuevo campo

    def __str__(self):
        return str(int(self.precio_proveedor))


class PedidoProveedor(models.Model):
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    formato = models.CharField(max_length=10)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pedido = models.DateField()
    fecha_entrega_prevista = models.DateField()

    def __str__(self):
        return f"{self.id} - {self.proveedor} - {self.tipo} - {self.nombre} - Cantidad: {self.cantidad} - Precio: {self.precio}"


    def save(self, *args, **kwargs):
        # Verificar si la cantidad es mayor que cero
        if self.cantidad > 0:
            super().save(*args, **kwargs)

            # Intentar obtener el objeto Stock existente
            stock = Stock.objects.filter(producto=self.producto).first()

            if stock is None:
                # Si no hay un objeto Stock existente, crear uno nuevo
                stock = Stock(producto=self.producto, cantidad=self.cantidad)
            else:
                # Si hay un objeto Stock existente, sumar la cantidad
                stock.cantidad = (stock.cantidad or 0) + self.cantidad

            # Establecer los demás valores del objeto Stock
            stock.formato = self.formato  # Ajusta según tus necesidades
            stock.precio_proveedor = self.precio  # Ajusta según tus necesidades
            stock.fecha_llegada_prevista = self.fecha_entrega_prevista
            stock.fecha_llegada_final = self.fecha_entrega_prevista

            # Guardar el objeto Stock
            stock.save()


class PedidoCliente(models.Model):
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    empresa = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='pedidos_empresa')
    zona = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_proveedor = models.ForeignKey('Stock', on_delete=models.CASCADE)
    gasto_almacen = models.DecimalField(max_digits=10, decimal_places=2)
    gasto_distribucion = models.DecimalField(max_digits=10, decimal_places=2)

    precio_final_kg = models.DecimalField(max_digits=10, decimal_places=2)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total_iva = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id} - Precio: {self.precio_final}"
    
    
    def calculate_prices(self):

        if self.cantidad <= 20:
            gasto_almacen =0.45   
        elif self.cantidad <= 50:
            gasto_almacen = 0.19
        elif self.cantidad <= 100:
            gasto_almacen = 0.12
        elif self.cantidad <= 200:
            gasto_almacen = 0.075
        elif self.cantidad <= 500:
            gasto_almacen = 0.046
        else:
            gasto_almacen = 0 
        
        self.gasto_almacen = gasto_almacen

        zona = self.zona
        if zona == 1:
            if self.cantidad <= 50:
                gasto_distribucion = 0.591
            elif self.cantidad <= 100:
                gasto_distribucion = 0.364
            elif self.cantidad <= 200:
                gasto_distribucion = 0.246
            elif self.cantidad <= 300:
                gasto_distribucion = 0.183
            elif self.cantidad <= 400:
                gasto_distribucion = 0.166
            elif self.cantidad <= 500:
                gasto_distribucion = 0.150
            elif self.cantidad <= 1000:
                gasto_distribucion = 0.120
            elif self.cantidad <= 2000:
                gasto_distribucion = 0.107
            else:
                gasto_distribucion = 0

        elif zona == 2:
            if self.cantidad <= 50:
                gasto_distribucion = 0.591
            elif self.cantidad <= 100:
                gasto_distribucion = 0.404
            elif self.cantidad <= 200:
                gasto_distribucion = 0.273
            elif self.cantidad <= 300:
                gasto_distribucion = 0.204
            elif self.cantidad <= 400:
                gasto_distribucion = 0.184
            elif self.cantidad <= 500:
                gasto_distribucion = 0.167
            elif self.cantidad <= 1000:
                gasto_distribucion = 0.133
            elif self.cantidad <= 2000:
                gasto_distribucion = 0.119
            else:
                gasto_distribucion = 0

        elif zona == 3:
            if self.cantidad <= 50:
                gasto_distribucion = 0.642
            elif self.cantidad <= 100:
                gasto_distribucion = 0.437
            elif self.cantidad <= 200:
                gasto_distribucion = 0.29
            elif self.cantidad <= 300:
                gasto_distribucion = 0.214
            elif self.cantidad <= 400:
                gasto_distribucion = 0.208
            elif self.cantidad <= 500:
                gasto_distribucion = 0.199
            elif self.cantidad <= 1000:
                gasto_distribucion = 0.192
            elif self.cantidad <= 2000:
                gasto_distribucion = 0.183
            else:
                gasto_distribucion = 0

        elif zona == 4:
            if self.cantidad <= 50:
                gasto_distribucion = 0.72
            elif self.cantidad <= 100:
                gasto_distribucion = 0.50
            elif self.cantidad <= 200:
                gasto_distribucion = 0.351
            elif self.cantidad <= 300:
                gasto_distribucion = 0.272
            elif self.cantidad <= 400:
                gasto_distribucion = 0.248
            elif self.cantidad <= 500:
                gasto_distribucion = 0.228
            elif self.cantidad <= 1000:
                gasto_distribucion = 0.201
            elif self.cantidad <= 2000:
                gasto_distribucion = 0.181
            else:
                gasto_distribucion = 0

        self.gasto_distribucion = gasto_distribucion

        # Calcular el precio final
        self.precio_final_kg = (self.precio_proveedor.precio_proveedor + Decimal(str(gasto_almacen)) + Decimal(str(gasto_distribucion)))
        self.precio_final = self.precio_final_kg * self.cantidad
        self.precio_total_iva = self.precio_final * Decimal('1.21')  # Asumiendo un IVA del 21%

    


    def save(self, *args, **kwargs):
        if self.cantidad > 0:
            self.calculate_prices()

            # Intentar obtener el objeto Stock existente
            stock = Stock.objects.filter(producto=self.producto).first()

            if stock is None:
                # Si no hay un objeto Stock existente, crear uno nuevo en negativo
                stock = Stock(producto=self.producto, cantidad=-self.cantidad, gasto_almacen=self.gasto_almacen)

            else:
                # Si hay un objeto Stock existente, restar la cantidad
                stock.cantidad = (stock.cantidad or 0) - self.cantidad
                stock.gasto_almacen = self.gasto_almacen  # Actualizar gasto_almacen en el objeto Stock

            # Guardar el objeto Stock
            stock.save()

            # Actualizar gasto_almacen en el objeto PedidoCliente
            self.gasto_almacen = stock.gasto_almacen

        # Llamar a super().save fuera del bloque if
        super().save(*args, **kwargs)





class Almacen(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    gdp = models.CharField(max_length=255)
    kg_20 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_50 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_100 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_200 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_500 = models.DecimalField(max_digits=10, decimal_places=2)

    def get_price_for_quantity(self, cantidad):
            
            if cantidad <= 20:
                return self.kg_20
            elif cantidad <= 50:
                return self.kg_50
            elif cantidad <= 100:
                return self.kg_100
            elif cantidad <= 200:
                return self.kg_200
            elif cantidad <= 500:
                return self.kg_500
            else:
                return 0


    def __str__(self):
        return f"{self.id} - {self.nombre}"


class Zona_1(models.Model):
    kg_50 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_100 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_200 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_300 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_400 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_500 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_1000 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_2000 = models.DecimalField(max_digits=10, decimal_places=2)

    def get_price_for_quantity(self, cantidad):

        if cantidad <= 50:
            return self.kg_50
        elif cantidad <= 100:
            return self.kg_100
        elif cantidad <= 200:
            return self.kg_200
        elif cantidad <= 300:
            return self.kg_300
        elif cantidad <= 400:
            return self.kg_400
        elif cantidad <= 500:
            return self.kg_500
        elif cantidad <= 1000:
            return self.kg_1000
        elif cantidad <= 2000:
            return self.kg_2000
        else:
            return 0


    def __str__(self):
        return f"{self.id}"
    

class Zona_2(models.Model):
    kg_50 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_100 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_200 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_300 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_400 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_500 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_1000 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_2000 = models.DecimalField(max_digits=10, decimal_places=2)

    def get_price_for_quantity(self, cantidad):

        if cantidad <= 50:
            return self.kg_50
        elif cantidad <= 100:
            return self.kg_100
        elif cantidad <= 200:
            return self.kg_200
        elif cantidad <= 300:
            return self.kg_300
        elif cantidad <= 400:
            return self.kg_400
        elif cantidad <= 500:
            return self.kg_500
        elif cantidad <= 1000:
            return self.kg_1000
        elif cantidad <= 2000:
            return self.kg_2000
        else:
            return 0



    def __str__(self):
        return f"{self.id}"
    

class Zona_3(models.Model):
    kg_50 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_100 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_200 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_300 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_400 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_500 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_1000 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_2000 = models.DecimalField(max_digits=10, decimal_places=2)

    def get_price_for_quantity(self, cantidad):

        if cantidad <= 50:
            return self.kg_50
        elif cantidad <= 100:
            return self.kg_100
        elif cantidad <= 200:
            return self.kg_200
        elif cantidad <= 300:
            return self.kg_300
        elif cantidad <= 400:
            return self.kg_400
        elif cantidad <= 500:
            return self.kg_500
        elif cantidad <= 1000:
            return self.kg_1000
        elif cantidad <= 2000:
            return self.kg_2000
        else:
            return 0



    def __str__(self):
        return f"{self.id}"
    

class Zona_4(models.Model):
    kg_50 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_100 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_200 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_300 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_400 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_500 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_1000 = models.DecimalField(max_digits=10, decimal_places=2)
    kg_2000 = models.DecimalField(max_digits=10, decimal_places=2)

    def get_price_for_quantity(self, cantidad):

        if cantidad <= 50:
            return self.kg_50
        elif cantidad <= 100:
            return self.kg_100
        elif cantidad <= 200:
            return self.kg_200
        elif cantidad <= 300:
            return self.kg_300
        elif cantidad <= 400:
            return self.kg_400
        elif cantidad <= 500:
            return self.kg_500
        elif cantidad <= 1000:
            return self.kg_1000
        elif cantidad <= 2000:
            return self.kg_2000
        else:
            return 0



    def __str__(self):
        return f"{self.id}"
    