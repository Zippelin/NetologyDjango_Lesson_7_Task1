from django.contrib import admin

# Register your models here.

from .models import Person, Advertisement


# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Advertisement)
# class AdvertisementAdmin(admin.ModelAdmin):
#     pass


admin.site.register(Person)
admin.site.register(Advertisement)