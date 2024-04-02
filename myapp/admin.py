from django.contrib import admin
from myapp import models

admin.site.register(models.Client)
admin.site.register(models.RegisterLocation)

class ImmobileImageInlineAdmin(admin.TabularInline):
    model = models.ImmobileImage
    extra = 0

class ImmobileAdmin(admin.ModelAdmin):
    inlines = [ImmobileImageInlineAdmin]

admin.site.register(models.Immobile, ImmobileAdmin)
