from django.contrib import admin
from .models import SupportedResourceType, MeKey


class SupportedResourceTypeAdmin(admin.ModelAdmin):

    list_display = (
        'resource_type',
        'database_name',
        'collection_name',
        'self_only')
    search_fields = ('resource_type', 'database_name', 'collection_name',)

admin.site.register(SupportedResourceType, SupportedResourceTypeAdmin)


class MeKeyAdmin(admin.ModelAdmin):

    list_display = ('user', 'resource_type', 'me_key', 'key_title')
    search_fields = ('user', 'resource_type', 'me_key', 'key_title')

admin.site.register(MeKey, MeKeyAdmin)
