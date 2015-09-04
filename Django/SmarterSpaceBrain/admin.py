from django.contrib import admin
from SmarterSpaceBrain.models import SpaceUser

# Register your models here.

class SpaceUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name']

admin.site.register(SpaceUser, SpaceUserAdmin)