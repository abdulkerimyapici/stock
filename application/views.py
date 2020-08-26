from django.shortcuts import render, HttpResponse
from .models import *
from django.db.models import Sum,Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
import decimal
from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import xml.etree.cElementTree as ET


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

@login_required
def home_view(request):
    args = {}
    args['stoklar'] = stoklar = Stoklar.objects.all().order_by('-urun_stok')

    args['stok_kategori'] = stok_kategori = StokKategori.objects.all()
    args['stok_alt_kategori'] = stok_alt_kategori = StokAltKategori.objects.all()
    page = request.GET.get('page', 1)
    page = int(page)
    args['last_exit'] = last_exit = int(stoklar.__len__() / 24)
    paginator = Paginator(stoklar, 24)
    index = paginator.page_range.index(paginator.num_pages)
    max_index = len(paginator.page_range)
    start_index = page - 3 if index >= 3 else 0
    end_index = page + 3 if page <= max_index - 3 else max_index
    if start_index <= 0:
        start_index = 0
        end_index = 6
    else:
        print(start_index)
    args['page_range'] = page_range = paginator.page_range[start_index:end_index]
    try:
        args['stoklar'] = paginator.page(page)
    except(EmptyPage):
        args['stoklar'] = paginator.page(page)  # Raises the same error

    args['toplam'] = Stoklar.objects.aggregate(Count('id'))
    args['stoktakiurunler'] = Stoklar.objects.aggregate(Sum('urun_stok'))
    args['azalanstoklar'] = azalanstoklar = Stoklar.objects.all()

    return render(request, 'base/base2.html', args)

@login_required
def stoguazalan(request):
    args = {}
    args['stoklar'] = stoklar = Stoklar.objects.filter(urun_stok__lt=2)
    args['stok_kategori'] = stok_kategori = StokKategori.objects.all()
    args['stok_alt_kategori'] = stok_alt_kategori = StokAltKategori.objects.all()
    args['toplam'] = stoklar.aggregate(Count('id'))
    args['stoktakiurunler'] = stoklar.aggregate(Sum('urun_stok'))

    return render(request, 'base/base2.html', args)

@login_required
@csrf_exempt
def urun_search(request):
    params = {}
    args = {}
    search_keys = []
    search_keys2 = []

    search = request.POST.get('search')
    key = request.POST.get('key')

    if search is None:
        search = ''

    if key == 'search':
        args['stok_kategori'] = stok_kategori = StokKategori.objects.all()
        args['stok_alt_kategori'] = stok_alt_kategori = StokAltKategori.objects.all()
        stoklar = Stoklar.objects.filter(Q(urun_adi__icontains=search) |
                                               Q(urun_no__icontains=search) |
                                               Q(urun_barkod_no__icontains=search)).distinct()
    elif key == 'kategori':
        args['stok_kategori'] = stok_kategori = StokKategori.objects.all()
        args['stok_alt_kategori'] = stok_alt_kategori = StokAltKategori.objects.filter(urun_urun_kategori_id = search)
        stoklar = Stoklar.objects.filter(urun_urun_stok_kategori_id = search)

    else:
        stoklar = {}

    for stok_alt in stok_alt_kategori:
        urun_alt_kategori = str(stok_alt.urun_alt_kategori)
        search_keys2.append({
        "urun_alt_kategori": urun_alt_kategori
    })

    for stok in stoklar:
        if isinstance(stok.urun_fiyat, Decimal):
            urun_fiyat = str(stok.urun_fiyat)
        else:
            urun_fiyat = stok.urun_fiyat
        urun_gorseli = str(stok.urun_gorseli)
        urun_urun_beden_adi = str(stok.urun_urun_beden_adi)
        urun_urun_rengi = str(stok.urun_urun_rengi)
        urun_alt_kategori = str(stok.urun_urun_stok_kategori)
        urun_kategori = str(stok.urun_urun_stok_alt_kategori)
        search_keys.append({
            "urun_barkod_no": stok.urun_barkod_no,
            "id": stok.id,
            "urun_adi": stok.urun_adi,
            "urun_no": stok.urun_no,
            "urun_fiyat": urun_fiyat,
            "urun_stok": stok.urun_stok,
            "urun_gorseli": urun_gorseli,
            "urun_urun_beden_adi": urun_urun_beden_adi,
            "urun_urun_rengi": urun_urun_rengi,
            "urun_alt_kategori": urun_alt_kategori,
            "urun_kategori": urun_kategori,
        })
    params['stoklar'] = search_keys
    params['alt_stoklar'] = search_keys2
    print(search_keys)
    print(search_keys2)
    return HttpResponse(json.dumps(params), content_type="application/json")

def login_view(request):
    return render(request, 'base/login.html')

def stok_table(request):
    args = {}
    args['stoklar'] = stoklar = Stoklar.objects.all().order_by('-urun_stok')
    args['stoklar'] = stok_kategori = StokKategori.objects.all()
    args['stoklar'] = stok_alt_kategori = StokAltKategori.objects.all()
    page = request.GET.get('page', 1)
    page = int(page)
    args['last_exit'] = last_exit = int(stoklar.__len__() / 24)
    paginator = Paginator(stoklar, 24)
    index = paginator.page_range.index(paginator.num_pages)
    max_index = len(paginator.page_range)
    start_index = page - 3 if index >= 3 else 0
    end_index = page + 3 if page <= max_index - 3 else max_index
    if start_index <= 0:
        start_index = 0
        end_index = 6
    else:
        print(start_index)
    args['page_range'] = page_range = paginator.page_range[start_index:end_index]
    try:
        args['stoklar'] = paginator.page(page)
    except(EmptyPage):
        args['stoklar'] = paginator.page(page)  # Raises the same error

    args['toplam'] = Stoklar.objects.aggregate(Count('id'))
    args['stoktakiurunler'] = Stoklar.objects.aggregate(Sum('urun_stok'))
    args['azalanstoklar'] = azalanstoklar = Stoklar.objects.all()
    return render(request, 'base/stoktable.html',args)

def login_check_view(request):
    kullanici_adi = request.POST.get('username_a')
    sifre = request.POST.get('password_a')
    user = authenticate(request,username=kullanici_adi, password=sifre)
    print(user)
    params = {}
    if user is not None:
        login(request, user)
        params['successs'] = "True"
        return HttpResponse(json.dumps(params), content_type="application/json")
    else:
        params['successs'] = "False"
        return HttpResponse(json.dumps(params), content_type="application/json")



def logout_view(request):
    logout(request)
    return render(request, 'base/login.html')

def xml_parse(request):

    args = {}
    args['stoklar'] = stoklar = Stoklar.objects.all()
    products = ET.Element("products")
    for stok in stoklar:
        product = ET.SubElement(products, "product")
        # categories = ET.SubElement(product, "categories")
        # features = ET.SubElement(product, "features")
        variants = ET.SubElement(product, "variants")
        images = ET.SubElement(product, "images")
        # feature = ET.SubElement(features, "feature")
        variant = ET.SubElement(variants, "variant")
        ET.SubElement(product,"id").text = str(stok.urun_barkod_no)
        ET.SubElement(product,"sku").text = str(stok.urun_barkod_no)
        ET.SubElement(product,"name").text = str(stok.urun_adi) + " " +  str(stok.urun_urun_rengi)
        ET.SubElement(product,"description").text = ""
        ET.SubElement(product,"brandId").text = str(stok.urun_barkod_no)
        ET.SubElement(product,"brandName").text = "NikkyMcBridget"
        # ET.SubElement(product,"categoryId").text = ""
        # ET.SubElement(product,"categoryName").text = ""
        ET.SubElement(product,"stock").text = str(stok.urun_stok)
        ET.SubElement(product,"price").text = str(stok.urun_fiyat)
        ET.SubElement(product,"priceNot").text = str(stok.urun_fiyat)
        ET.SubElement(product,"cost").text = ""
        ET.SubElement(product,"tax").text = ""
        # ET.SubElement(categories,"category").text = ""
        # # ET.SubElement(categories,"category").text = ""
        # ET.SubElement(feature,"name").text = ""
        # ET.SubElement(feature,"value").text = ""
        ET.SubElement(variant,"id").text = str(stok.urun_barkod_no)
        ET.SubElement(variant,"sku").text = str(stok.urun_barkod_no)
        ET.SubElement(variant,"stock").text = str(stok.urun_stok)
        ET.SubElement(variant,"label").text = str(stok.urun_urun_beden_adi)
        ET.SubElement(variant,"barcode").text = str(stok.urun_barkod_no)
        # ET.SubElement(images,"image").text = str(stok.urun_gorseli)
        ET.SubElement(images,"image").text = " "

    tree = ET.ElementTree(products)
    tree.write("media/stok_xml.xml")
    response = HttpResponse(open("media/stok_xml.xml", 'rb').read())
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = 'attachment; filename=media/stok_xml.xml'

    return response
    # return render(request, 'base/base2.html', args)





