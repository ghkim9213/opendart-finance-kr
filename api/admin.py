from .models import *
from django.contrib import admin

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    pass

@admin.register(ContentTag)
class ContentTagAdmin(admin.ModelAdmin):
    pass

@admin.register(ContentParameter)
class ContentParameterAdmin(admin.ModelAdmin):
    pass

@admin.register(ContentResponse)
class ContentResponseAdmin(admin.ModelAdmin):
    pass
