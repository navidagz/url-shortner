from django.contrib import admin

from analytics.models import Analytics, Browser, Device

admin.site.register(Analytics)
admin.site.register(Browser)
admin.site.register(Device)
