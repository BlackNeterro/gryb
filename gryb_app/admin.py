from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, CarouselImage, Cart, Order, Comment, Video

admin.site.register(Product)
admin.site.register(CarouselImage)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Comment)
admin.site.register(Video)

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'name', 'phone_number', 'address']
    fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal Info', {'fields': ('name', 'phone_number', 'address')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    ('Important dates', {'fields': ('last_login', 'date_joined')}),
)

admin.site.register(User, CustomUserAdmin)

