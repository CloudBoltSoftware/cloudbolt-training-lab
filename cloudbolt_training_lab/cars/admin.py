from django.contrib import admin
from .models import *


class ManufacturerAdmin(admin.ModelAdmin):
    fields = ['manufacturer']


class MakeAdmin(admin.ModelAdmin):
    fields = ['make', 'manufacturer']


class TrimAdmin(admin.ModelAdmin):
    fields = ['trim', 'make']


admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Make, MakeAdmin)
admin.site.register(Trim, TrimAdmin)
