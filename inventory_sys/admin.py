from django.contrib import admin
from .models import item_type, inventory, brand

admin.site.register(brand)
admin.site.register(inventory)
admin.site.register(item_type)