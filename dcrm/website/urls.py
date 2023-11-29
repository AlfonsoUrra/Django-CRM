from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('logout/',views.logout_user, name = 'logout'),
    path('register/',views.register_user, name = 'register'),
    path('record/<int:pk>',views.customer_record, name = 'record'),
    path('supplier/<int:pk>',views.supplier_record, name = 'supplier'),
    path('product/<int:pk>',views.product, name = 'product'),

    path('add_record/',views.add_record, name = 'add_record'),
    path('add_supplier/',views.add_supplier, name = 'add_supplier'),
    path('add_product/',views.add_product, name = 'add_product'),
    
    path('delete_record/<int:pk>',views.delete_record, name = 'delete_record'),
    path('delete_supplier/<int:pk>',views.delete_supplier, name = 'delete_supplier'),
    path('delete_product/<int:pk>',views.delete_product, name = 'delete_product'),
    path('delete_order_supplier/<int:pk>',views.delete_order_supplier, name = 'delete_order_supplier'),
    path('delete_order_client/<int:pk>',views.delete_order_client, name = 'delete_order_client'),
    path('delete_stock/<int:pk>',views.delete_stock, name = 'delete_stock'),

    path('update_supplier/<int:pk>',views.update_supplier, name = 'update_supplier'),
    path('update_record/<int:pk>',views.update_record, name = 'update_record'),
    path('update_product/<int:pk>',views.update_product, name = 'update_product'),
    path('update_order_supplier/<int:pk>',views.update_order_supplier, name = 'update_order_supplier'),
    path('update_order_client/<int:pk>',views.update_order_client, name = 'update_order_client'),
    path('update_stock/<int:pk>',views.update_stock, name = 'update_stock'),

    path('order_client_card/<int:pk>',views.order_client_card, name = 'order_client_card'),
    path('order_supplier_card/<int:pk>',views.order_supplier_card, name = 'order_supplier_card'),
    path('stock_card/<int:pk>',views.stock_card, name = 'stock_card'),


    path('add_order_client/',views.add_order_client, name = 'add_order_client'),
    path('add_order_supplier/',views.add_order_supplier, name = 'add_order_supplier'),
    path('add_stock/',views.add_stock, name = 'add_stock'),

    path('order_clients/',views.order_clients, name = 'order_clients'),
    path('order_suppliers/',views.order_suppliers, name = 'order_suppliers'),

    path('stock/',views.stock, name = 'stock'),


]


