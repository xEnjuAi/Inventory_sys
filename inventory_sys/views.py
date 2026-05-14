from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from .models import brand, inventory, item_type


def inventory_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        inventory_qs = inventory.objects.filter(
            Q(full_name__icontains=search_query) | 
            Q(username__icontains=search_query)
        ).order_by('-inventory_id')
    else:
        inventory_qs = inventory.objects.all().order_by('-inventory_id')

    paginator = Paginator(inventory_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/InventoryList.html', {
        'page_obj': page_obj, 
        'search_query': search_query
    })


def add_inventory(request):
    item_types = item_type.objects.all()
    brands = brand.objects.all()
    
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_type_id = request.POST.get('item_type')
        brand_id = request.POST.get('brand')
        recieved_date = request.POST.get('recieved_date')
        stock = request.POST.get('stock')
        shipper = request.POST.get('shipper')
        item_picture = request.FILES.get('profile_picture') 

        if inventory.objects.filter(item_name=item_name).exists():
            messages.error(request, f'Item name "{item_name}" is already taken! Please choose another one.')
            return redirect('add_inventory')

        if not stock or len(stock) == 0 or not stock.isdigit():
            messages.error(request, 'Enter a valid stock number (e.g., 100).')
            return redirect('add_inventory')

        brand_instance = get_object_or_404(brand, pk=brand_id)
        item_type_instance = get_object_or_404(item_type, pk=item_type_id)

        inventory.objects.create(
            item_name=item_name,
            item_type=item_type_instance,
            brand=brand_instance,
            recieved_date=recieved_date,
            stock=stock,
            shipper=shipper,
            item_picture=item_picture
        )
        
        messages.success(request, 'Item successfully added!')
        return redirect('inventory_list')
        
    return render(request, 'inventory/AddInventory.html', {'item_types': item_types, 'brands': brands})


def edit_inventory(request, inventory_id):
    inventory_item = get_object_or_404(inventory, pk=inventory_id)
    item_types = item_type.objects.all()
    brands = brand.objects.all()

    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_type_id = request.POST.get('item_type')
        brand_id = request.POST.get('brand')
        recieved_date = request.POST.get('recieved_date')
        stock = request.POST.get('stock')
        shipper = request.POST.get('shipper')
        item_picture = request.FILES.get('item_picture')
        
        if inventory.objects.filter(item_name=item_name).exclude(pk=inventory_id).exists():
            messages.error(request, f'Item name "{item_name}" is already taken!')
            return redirect('edit_inventory', inventory_id=inventory_id)

        if len(stock) == 0 or not stock.isdigit() or not stock.startswith('enter number'):
            messages.error(request, 'Enter a valid stock number (e.g., 100).')
            return redirect('edit_inventory', inventory_id=inventory_id)

        inventory_item.item_name = item_name
        inventory_item.item_type = get_object_or_404(item_type, pk=item_type_id)
        inventory_item.brand = get_object_or_404(brand, pk=brand_id)
        inventory_item.recieved_date = recieved_date
        inventory_item.stock = stock
        inventory_item.shipper = shipper
        inventory_item.item_picture = item_picture
        inventory_item.save()
        messages.success(request, 'Item updated successfully!')
        return redirect('inventory_list')   

        if item_picture:
            inventory_item.item_picture = item_picture
        inventory_item.save()
        messages.success(request, 'Item updated successfully!')
        return redirect('inventory_list')

    return render(request, 'inventory/EditInventory.html', {'inventory_item': inventory_item, 'item_types': item_types, 'brands': brands})


def delete_inventory(request, inventory_id):
    inventory_item = get_object_or_404(inventory, pk=inventory_id)
    if request.method == 'POST':
        inventory_item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('inventory_list')
    return render(request, 'inventory/DeleteInventory.html', {'inventory_item': inventory_item})

#break

def item_type_list(request):
    item_types = item_type.objects.all()
    return render(request, 'item_type/ItemTypesList.html', {'item_types': item_types})

def add_item_type(request):
    if request.method == 'POST':
        item_type_name = request.POST.get('item_type')
        if item_type_name:
            item_type.objects.create(item_type=item_type_name)
            messages.success(request, 'Item type added successfully!')
            return redirect('item_type_list')
    return render(request, 'item_type/AddItemType.html')

def edit_item_type(request, item_type_id):
    item_type_obj = get_object_or_404(item_type, pk=item_type_id)
    if request.method == 'POST':
        item_type_obj.item_type = request.POST.get('item_type')
        item_type_obj.save()
        messages.success(request, 'Item type updated successfully!')
        return redirect('item_type_list')
    return render(request, 'item_type/EditItemType.html', {'item_type': item_type_obj})

def delete_item_type(request, item_type_id):
    item_type_obj = get_object_or_404(item_type, pk=item_type_id)
    if request.method == 'POST':
        item_type_obj.delete()
        messages.success(request, 'Item type deleted successfully!')
        return redirect('item_type_list')
    return render(request, 'item_type/DeleteItemType.html', {'item_type': item_type_obj})

# break

def brand_list(request):
    brands = brand.objects.all()
    return render(request, 'brand/BrandsList.html', {'brands': brands})

def add_brand(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand')
        if brand_name:
            brand.objects.create(brand=brand_name)
            messages.success(request, 'Brand added successfully!')
            return redirect('brand_list')
    return render(request, 'brand/AddBrand.html')

def edit_brand(request, brand_id):
    brand_obj = get_object_or_404(brand, pk=brand_id)
    if request.method == 'POST':
        brand_obj.brand = request.POST.get('brand')
        brand_obj.save()
        messages.success(request, 'Brand updated successfully!')
        return redirect('brand_list')
    return render(request, 'brand/EditBrand.html', {'brand': brand_obj})

def delete_brand(request, brand_id):
    brand_obj = get_object_or_404(brand, pk=brand_id)
    if request.method == 'POST':
        brand_obj.delete()
        messages.success(request, 'Brand deleted successfully!')
        return redirect('brand_list')
    return render(request, 'brand/DeleteBrand.html', {'brand': brand_obj})