from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, AddSupplierForm, AddProductForm, AddPedidoClienteForm, AddPedidoProveedorForm, AddStockForm
from .models import Cliente, Proveedor, Producto, PedidoProveedor, PedidoCliente, Stock, Almacen

def home(request):
    records = Cliente.objects.all()
    supplier = Proveedor.objects.all()
    product = Producto.objects.all()
    # check if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login user
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - Please try again'))
            return redirect('home')
    
    else:
        return render(request, 'home.html', {'records': records, 'supplier': supplier, 'product': product})
    
def order_clients(request):
    records = PedidoCliente.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login user
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - Please try again'))
            return redirect('home')
    else:
        return render(request, 'order_clients.html', {'records': records})
        
def order_suppliers(request):
    records = PedidoProveedor.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login user
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - Please try again'))
            return redirect('home')
    else:  
        return render(request, 'order_suppliers.html', {'records': records})
    
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            # login user
            login(request, user)
            messages.success(request, ('You have registered...'))
            return redirect('home')
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})



def customer_record(request, pk):
    if request.user.is_authenticated:
        custumer_record = Cliente.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': custumer_record})
    else:
        messages.success(request, ('Please login to view customer record'))
        return redirect('home')

def supplier_record(request, pk):
    if request.user.is_authenticated:
        supplier_record = Proveedor.objects.get(id=pk)
        return render(request, 'supplier.html', {'supplier_record': supplier_record})
    else:
        messages.success(request, ('Please login to view supplier record'))
        return redirect('home')

def product(request, pk):
    if request.user.is_authenticated:
        product = Producto.objects.get(id=pk)
        return render(request, 'product.html', {'product': product})
    else:
        messages.success(request, ('Please login to view products'))
        return redirect('home')



def order_supplier_card(request, pk):
    if request.user.is_authenticated:
        order_supplier_card = PedidoProveedor.objects.get(id=pk)
        return render(request, 'order_supplier_card.html', {'order_supplier_card': order_supplier_card})
    else:
        messages.success(request, ('Please login to view order'))
        return redirect('home')
    
def order_client_card(request, pk):
    if request.user.is_authenticated:
        order_client_card = PedidoCliente.objects.get(id=pk)
        return render(request, 'order_client_card.html', {'order_client_card': order_client_card})
    else:
        messages.success(request, ('Please login to view order'))
        return redirect('home')
    
def stock_card(request, pk):
    if request.user.is_authenticated:
        stock_card = Stock.objects.get(id=pk)
        return render(request, 'stock_card.html', {'stock_card': stock_card})
    else:
        messages.success(request, ('Please login to view stock'))
        return redirect('home')




def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Cliente.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ('Customer Record has been deleted'))
        return redirect('home')
    else:
        messages.success(request, ('Please login to delete customer record'))
        return redirect('home')
    
def delete_supplier(request, pk):
    if request.user.is_authenticated:
        delete_it = Proveedor.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ('Supplier Record has been deleted'))
        return redirect('home')
    else:
        messages.success(request, ('Please login to delete supplier record'))
        return redirect('home')
    
def delete_product(request, pk):
    if request.user.is_authenticated:
        delete_it = Producto.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ('Product has been deleted'))
        return redirect('home')
    else:
        messages.success(request, ('Please login to delete product'))
        return redirect('home')
    
def delete_order_supplier(request, pk):
    if request.user.is_authenticated:
        delete_it = PedidoProveedor.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ('Order has been deleted'))
        return redirect('order_suppliers')
    else:
        messages.success(request, ('Please login to delete order'))
        return redirect('order_suppliers')
    
def delete_order_client(request, pk):
    if request.user.is_authenticated:
        delete_it = PedidoCliente.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ('Order has been deleted'))
        return redirect('order_clients')
    else:
        messages.success(request, ('Please login to delete order'))
        return redirect('order_clients')
    
def delete_stock(request, pk):
    if request.user.is_authenticated:
        delete_it = Stock.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, ('Stock has been deleted'))
        return redirect('stock')
    else:
        messages.success(request, ('Please login to delete stock'))
        return redirect('stock')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')
    
def add_supplier(request):
    form = AddSupplierForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_supplier = form.save()
                messages.success(request, "Supplier Added...")
                return redirect('home')
        return render(request, 'add_supplier.html', {'form':form})
    
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')
    
def add_product(request):
    form = AddProductForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_product = form.save()
                messages.success(request, "Product Added...")
                return redirect('home')
        return render(request, 'add_product.html', {'form':form})
    
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')
    
def add_order_client(request):
    form = AddPedidoClienteForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_order_client = form.save()
                messages.success(request, "Order Added...")
                return redirect('order_clients')
        return render(request, 'add_order_client.html', {'form':form})
    
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')
    
def add_order_supplier(request):
    form = AddPedidoProveedorForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Order Added...")
                return redirect('order_suppliers')

        return render(request, 'add_order_supplier.html', {'form': form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')

def add_stock(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddStockForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Stock Added...")
                return redirect('stock')
        else:
            form = AddStockForm()

        return render(request, 'add_stock.html', {'form': form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')    



def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Cliente.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, ('Record has been updated'))
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, ('Please login to update customer record'))
        return redirect('home')

def update_supplier(request, pk):
    if request.user.is_authenticated:
        current_supplier = Proveedor.objects.get(id=pk)
        form = AddSupplierForm(request.POST or None, instance=current_supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier record has been updated')
            return redirect('home')
        return render(request, 'update_supplier.html', {'form': form})
    else:
        messages.success(request, 'Please login to update supplier record')
        return redirect('home')
    
def update_product(request, pk):
    if request.user.is_authenticated:
        current_product = Producto.objects.get(id=pk)
        form = AddProductForm(request.POST or None, instance=current_product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product record has been updated')
            return redirect('home')
        return render(request, 'update_product.html', {'form': form})
    else:
        messages.success(request, 'Please login to update product record')
        return redirect('home')

def update_stock(request, pk):
    if request.user.is_authenticated:
        current_stock = Stock.objects.get(id=pk)
        form = AddStockForm(request.POST or None, instance=current_stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock record has been updated')
            return redirect('stock')
        return render(request, 'update_stock.html', {'form': form})
    else:
        messages.success(request, 'Please login to update stock record')
        return redirect('stock')

def update_order_supplier(request, pk):
    if request.user.is_authenticated:
        current_order_supplier = PedidoProveedor.objects.get(id=pk)
        form = AddPedidoProveedorForm(request.POST or None, instance=current_order_supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order has been updated')
            return redirect('order_suppliers')
        return render(request, 'update_order_supplier.html', {'form': form})
    else:
        messages.success(request, 'Please login to update order')
        return redirect('order_suppliers')
    
def update_order_client(request, pk):
    if request.user.is_authenticated:
        current_order_client = PedidoCliente.objects.get(id=pk)
        form = AddPedidoClienteForm(request.POST or None, instance=current_order_client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order has been updated')
            return redirect('order_clients')
        return render(request, 'update_order_client.html', {'form': form})
    else:
        messages.success(request, 'Please login to update order')
        return redirect('order_clients')

        

def stock(request):
    records = Stock.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login user
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - Please try again'))
            return redirect('home')
    else:
        return render(request, 'stock.html', {'records': records})




