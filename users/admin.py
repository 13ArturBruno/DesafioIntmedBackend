from django.contrib import admin

# Register your models here.
from users.models import User


class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'email']


admin.site.register(User, UserAdmin)