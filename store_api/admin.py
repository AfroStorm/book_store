from django.contrib import admin
from store_api import models

# Register your models here.


admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Profile)
admin.site.register(models.Tag)
