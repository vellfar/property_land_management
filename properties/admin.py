from django.contrib import admin
from .models import Document, Location, LandProperty, OwnershipTransfer

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'store_name', 'original_name', 'uploaded_date', 'document_type', 'purpose', 'status', 'uploaded_by')
    list_filter = ('document_type', 'status', 'uploaded_date')
    search_fields = ('store_name', 'original_name', 'purpose', 'uploaded_by__username')
    ordering = ('-uploaded_date',)
    date_hierarchy = 'uploaded_date'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'village', 'parish', 'sub_county', 'county', 'district', 'country', 'status', 'created_at', 'updated_at')
    list_filter = ('district', 'country', 'status')
    search_fields = ('village', 'parish', 'sub_county', 'county', 'district', 'country')
    ordering = ('district', 'county')
    date_hierarchy = 'created_at'

@admin.register(LandProperty)
class LandPropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'PID', 'owner', 'location', 'size', 'valuation', 'status', 'added_by', 'created_at', 'updated_at')
    list_filter = ('status', 'valuation', 'size', 'created_at')
    search_fields = ('name', 'PID', 'owner__username', 'location__village', 'added_by__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

@admin.register(OwnershipTransfer)
class OwnershipTransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_id', 'current_owner', 'new_owner', 'request_date', 'status', 'added_by', 'created_at', 'updated_at')
    list_filter = ('status', 'request_date', 'created_at')
    search_fields = ('property_id__name', 'current_owner__username', 'new_owner__username', 'added_by__username')
    ordering = ('-request_date',)
    date_hierarchy = 'request_date'
