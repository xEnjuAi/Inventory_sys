from django.urls import path
from . import views

urlpatterns = [
    # INVENTORY URLS
    path('', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.add_inventory, name='add_inventory'),
    path('inventory/edit/<int:inventory_id>/', views.edit_inventory, name='edit_inventory'),
    path('inventory/delete/<int:inventory_id>/', views.delete_inventory, name='delete_inventory'),

    # ITEM TYPE URLS
    path('item_type/list/', views.item_type_list, name='item_type_list'),
    path('item_type/add/', views.add_item_type, name='add_item_type'),
    path('item_type/edit/<int:item_type_id>/', views.edit_item_type, name='edit_item_type'),
    path('item_type/delete/<int:item_type_id>/', views.delete_item_type, name='delete_item_type'),

    # BRAND URLS
    path('brand/list/', views.brand_list, name='brand_list'),
    path('brand/add/', views.add_brand, name='add_brand'),
    path('brand/edit/<int:brand_id>/', views.edit_brand, name='edit_brand'),
    path('brand/delete/<int:brand_id>/', views.delete_brand, name='delete_brand'),
]