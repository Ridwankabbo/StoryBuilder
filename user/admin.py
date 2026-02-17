from django.contrib import admin
from .models import User
# Register your models here.

class UserAdminView(admin.ModelAdmin):
    
    list_display = ('id', 'username', 'email', 'is_active', 'is_admin', 'created_at')

    search_fields = ('id', 'email')
    
    
admin.site.register(User, UserAdminView)