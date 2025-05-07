from django.contrib import admin
from .models import State,District,Taluk,RevenueVillage,Plot,OrderItem,Order,CartItem

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Display ID and name in the admin panel
    search_fields = ('name',)  # Allow search by name
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
@admin.register(Taluk)
class TalukAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    list_filter = ('district',)

@admin.register(RevenueVillage)
class RevenueVillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'taluk')
    list_filter = ('taluk',)

from django.contrib import admin
from django.utils.html import format_html
from .models import Plot

@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = (
        'plot_number', 'survey_no', 'subdivision', 'owner','facing','dimensions',
        'state', 'district', 'taluk', 'revenue_village', 
        'price_range', 'land_image_thumbnail'
    )
    search_fields = (
        'plot_number', 'owner', 'state', 
        'district', 'taluk', 'revenue_village'
    )
    list_filter = ('state', 'district', 'taluk', 'revenue_village')
    readonly_fields = ('land_image_preview',)  # Read-only field for image preview in detail/edit views

    fieldsets = (
        ('Plot Information', {
            'fields': (
                'state', 'district', 'taluk', 'revenue_village', 'owner','facing','dimensions',
                'survey_no', 'subdivision', 'plot_number', 'price_range',
                'land_image', 'land_image_preview'
            )
        }),
    )

    # Display thumbnail in the list view
    def land_image_thumbnail(self, obj):
        if obj.land_image:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.land_image.url)
        return "No Image"
    land_image_thumbnail.short_description = 'Thumbnail'

    # Display full image preview in the detail/edit view
    def land_image_preview(self, obj):
        if obj.land_image:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%;"/>', obj.land_image.url)
        return "No Image"
    land_image_preview.short_description = 'Land Image Preview'



# Customize the admin for CartItem
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'plot')  # Fields to display
    search_fields = ('user__username', 'plot__plot_number')  # Searchable fields
    list_filter = ('user', 'plot')  # Filters on the side
    ordering = ('user',)  # Default ordering

# Customize the admin for Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')  # Fields to display
    search_fields = ('user__username',)  # Searchable fields
    list_filter = ('created_at',)  # Filters on the side
    ordering = ('-created_at',)  # Default ordering

# Customize the admin for OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'plot', 'price')  # Fields to display
    search_fields = ('order__id', 'plot__plot_number')  # Searchable fields
    list_filter = ('order',)  # Filters on the side
    ordering = ('order',)  # Default ordering