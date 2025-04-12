from django.contrib import admin
from ..corecode.models import SiteConfig  

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "value")  
    search_fields = ("key", "value")  


