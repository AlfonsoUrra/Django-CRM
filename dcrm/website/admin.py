from django.contrib import admin
from .models import Proveedor, Producto, DetallePedido, Almacen, Zona, CosteEnvio, Pedido, Cliente

admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(DetallePedido)
admin.site.register(Almacen)
admin.site.register(Zona)
admin.site.register(CosteEnvio)
admin.site.register(Pedido)
admin.site.register(Cliente)