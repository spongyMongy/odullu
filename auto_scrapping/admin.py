from django.contrib import admin

from auto_scrapping.models import GiftModelAutoScraping, GiftModelUserEntry

# Register your models here.
admin.site.register(GiftModelAutoScraping)

# class AutoScrapingAdmin(admin.ModelAdmin):
#     list_display = ['link  ', 'time', 'gift_name', 'thumbnail_link']
#
#
# admin.site.register(GiftModelAutoScraping, AutoScrapingAdmin)