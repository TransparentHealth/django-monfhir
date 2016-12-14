from django.contrib import admin
from .models import SupportedResourceType

class SupportedResourceTypeAdmin(admin.ModelAdmin):
    
    list_display =  ('resource_type', 'database_name', 'collection_name', 'self_only')
    search_fields = ('resource_type', 'database_name', 'collection_name',  )
    
admin.site.register(SupportedResourceType, SupportedResourceTypeAdmin)
