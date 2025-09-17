from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Product, ProductPiece, ProductImage, Order, OrderItem, CreditCard, ProductReview

#  CustomUser 
class AdminCustomUser(UserAdmin):
    model = CustomUser
    list_display = ['id', 'get_full_name', 'email', 'cpf']
    list_display_links = ('id', 'get_full_name', 'email', 'cpf')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Monitoring', {'fields': ('last_login', 'date_joined')}),
        ('User Data', {'fields': ('first_name', 'last_name', 'cpf',
                                  'address_country','address_state','address_city',
                                  'address_district','address_street','address_number','address_zip_code')}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','first_name','last_name','cpf',
                       'address_country','address_state','address_city',
                       'address_district','address_street','address_zip_code',
                       'address_number','password1','password2'),
        }),
    )
    ordering = ['email']

#  Product 
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_category', 'price', 'stock')
    list_filter = ('category',)

    def get_category(self, obj):
        return obj.category.name if obj.category else "-"
    get_category.short_description = 'Categoria'


class ProductPieceAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'weight', 'measurements')
    list_filter = ('product',)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url', 'is_main')
    list_filter = ('product', 'is_main')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')


class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('order', 'card_number', 'holder_name', 'expiration_date')


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('product', 'rating')


#  Registro 
admin.site.register(CustomUser, AdminCustomUser)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPiece, ProductPieceAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
