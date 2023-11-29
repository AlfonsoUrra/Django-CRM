from django.contrib import admin
from .models import Proveedor, Cliente, Producto, Stock, PedidoProveedor, PedidoCliente, Almacen,Zona_1, Zona_2, Zona_3, Zona_4

admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Stock)
admin.site.register(PedidoProveedor)
admin.site.register(PedidoCliente)
admin.site.register(Almacen)
admin.site.register(Zona_1)
admin.site.register(Zona_2)
admin.site.register(Zona_3)
admin.site.register(Zona_4)

