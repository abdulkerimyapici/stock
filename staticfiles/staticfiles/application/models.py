from django.db import models

# Create your models here.


class urun_beden_tanim(models.Model):
    urun_beden_adi = models.CharField(max_length=10, verbose_name='urun_beden_adi' ,blank=True, null=True)
    urun_beden_kisa_kodu = models.CharField(max_length=10, verbose_name='urun_beden_kisa_kodu' ,blank=True, null=True)

    class Meta:
        verbose_name = 'Beden'
        verbose_name_plural = 'Bedenler'

    def __str__(self):
        return self.urun_beden_adi

class urun_renk_tanim(models.Model):
    urun_beden_rengi = models.CharField(max_length=10, verbose_name='urun_beden_rengi', blank=True, null=True,default='1')

    class Meta:
        verbose_name = 'Renk'
        verbose_name_plural = 'Renkler'

    def __str__(self):
        return self.urun_beden_rengi

class StokKategori(models.Model):
    urun_kategori = models.CharField(max_length=255, verbose_name='urun_kategori', blank=True, null=True)

    class Meta:
        verbose_name = 'Stok Kategori'
        verbose_name_plural = 'Stok Kategorileri'

    def __str__(self):
        return self.urun_kategori

class StokAltKategori(models.Model):
    urun_alt_kategori = models.CharField(max_length=255, verbose_name='urun_alt_kategori', blank=True, null=True)
    urun_urun_kategori = models.ForeignKey(StokKategori, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Stok Alt Kategori'
        verbose_name_plural = 'Stok Alt Kategorileri'

    def __str__(self):
        return self.urun_alt_kategori



class Stoklar(models.Model):
    urun_barkod_no = models.CharField(max_length=255,blank=True, verbose_name='urun_barkod_no', null=True)
    urun_adi = models.CharField(max_length=255,blank=True, verbose_name='urun_adi', null=True)
    urun_no = models.CharField(max_length=255,blank=True,verbose_name='urun_no', null=True)
    urun_fiyat = models.DecimalField(max_digits=5, decimal_places=2)
    urun_stok = models.IntegerField(blank=True,verbose_name='urun_stok_durumu', null=True)
    urun_gorseli = models.FileField(max_length=255,blank=True, verbose_name='urun_gorseli', null=True, default='resimYokUrun.jpg')
    urun_urun_rengi = models.ForeignKey(urun_renk_tanim, on_delete=models.CASCADE)
    urun_urun_beden_adi = models.ForeignKey(urun_beden_tanim, on_delete=models.CASCADE)
    urun_urun_stok_alt_kategori = models.ForeignKey(StokAltKategori, on_delete=models.CASCADE)
    urun_urun_stok_kategori = models.ForeignKey(StokKategori, on_delete=models.CASCADE)
    urun_kayit_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Stok'
        verbose_name_plural = 'Stoklar'
