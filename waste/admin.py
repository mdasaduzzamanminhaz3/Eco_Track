from django.contrib import admin
from .models import WasteCategory, PickupRequest

@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'carbon_multiplier', 'points_multiplier')
    search_fields = ('name',)

@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recycler', 'category', 'estimated_weight', 'actual_weight', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('user__email', 'recycler__email', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')