from django.db import models

class item_type(models.Model):
    item_type_id = models.BigAutoField(primary_key=True)
    item_type = models.CharField(max_length=55, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_item_types'

    def __str__(self):
        return self.item_type

class brand(models.Model):
    brand_id = models.BigAutoField(primary_key=True)
    brand = models.CharField(max_length=55, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_brands'

    def __str__(self):
        return self.brand
        

class inventory(models.Model):
    inventory_id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=55, blank=False)
    item_type = models.ForeignKey(item_type, on_delete=models.CASCADE)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)
    recieved_date = models.DateField(blank=False)
    shipper = models.CharField(max_length=255, blank=False)
    Stock = models.CharField(max_length=255, blank=False)
    
    item_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_inventory'