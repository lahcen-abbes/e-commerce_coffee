from django.shortcuts import get_object_or_404, render #get_object_or_404 me3netha jibli object li rani baghih(lien) yla mkach affichili This page could not be found.
from datetime import datetime
from .models import Product

# Create your views here.

def products(request): #b request hada njibo les valeurs
    pro = Product.objects.all()
    name = None #drnah none psq te7t fl context rana dayrin 'name':name imaginer manach faurin had instruction w dkhelna fi kach autre lien w massabch 'searchname' in request.GET ye3tina error bsh kon ndiro name = None netfadaw l'erreur 
    desc = None
    pfrom = None
    pto = None
    cs = None #case sensitive ta3 7assassiyet al a7rof ye3tni 7erf capital machi kima small

    if 'cs' in request.GET :
        cs = request.GET['cs']
        if not cs : #yla ma3alemch 3liha tweli off
            cs = "off"
    if 'searchname' in request.GET : #if searchname rahi mewjoda fl lien, 3lah drnaha psq kon neketbo fl lien http://127.0.0.1:8000/products/?searchname=espresso w n3ewdo nedekhlo fl http://127.0.0.1:8000/products/ ye3tina error psq dayer fi baleh mazal searchname=espresso téxister, tsam drna had condition bach yweli searchname yekhroj f lien juste ki ndiro submit
        name = request.GET['searchname'] #searchname hiya name li fl input ta3 Product Name Contains li fl search.html, hna name treprésenter la valeur li ydekhelha user fl input ta3 searchname
        if name: #bach net2ekdo bki name marahch khawi
            if cs=="on" :
                pro = pro.filter(name__contains=name) #ki ndiro contains bl i tsama tweli tet7esses mel 7orof yla capital wla small
            else :
                pro = pro.filter(name__icontains=name) #hna drna filter lel name li lfog w hadi __ zednaha psq li ndiro 3liha filter nzidohalha django haka yekhdem, tsama golnaleh 3tina objects li name ta3hom kima name li user dekhleh
    
    if 'searchdesc' in request.GET :
        desc=request.GET['searchdesc']
        if desc :
            if cs=="on" :
                pro = pro.filter(description__contains=desc)
            else :
                pro = pro.filter(description__icontains=desc)
    
    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET:
        pfrom = request.GET['searchpricefrom']
        pto = request.GET['searchpriceto']
        if pfrom and pto :
            if pfrom.isdigit() and pto.isdigit() : #drna isdigit bach net2ekdo beli dakhel ar9am
                pro = pro.filter( price__gte = pfrom , price__lte = pto ) #gte: greater then, lte: lower then

    context = {
        'products': pro ,
        #'name':name #la variable name li rahi lfog drnaha f 'name'
    }
    return render(request, 'products/products.html', context)

def product(request, pro_id):
    context = {
        'pro' : get_object_or_404(Product, pk=pro_id) #kima ne3erfo f database f pgAdmin products ga3 mre9min bl id(pro_id), tsama hna golnaleh hawes 3la a product b id ta3h f database yla massebtehch dirlna error 404 page not be found.
    }
    return render(request, 'products/product.html', context)

def search(request):
    return render(request, 'products/search.html')
