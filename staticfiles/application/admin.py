from django.contrib import admin
from .models import *
# Register your models here.


class StokAdmin(admin.ModelAdmin):

    list_display = ['urun_barkod_no', 'urun_adi', 'urun_kayit_tarihi', 'urun_urun_beden_adi','urun_urun_rengi']
    list_display_links = ['urun_barkod_no','urun_adi', 'urun_kayit_tarihi',  'urun_urun_beden_adi','urun_urun_rengi']
    list_filter = ['urun_adi', 'urun_kayit_tarihi',  'urun_urun_rengi']
    search_fields =  ['urun_barkod_no','urun_adi']

    class Meta:
        model = Stoklar


admin.site.register(Stoklar, StokAdmin)
# admin.site.register(StokAdmin)
admin.site.register(StokKategori)
admin.site.register(StokAltKategori)
admin.site.register(urun_beden_tanim)
admin.site.register(urun_renk_tanim)

