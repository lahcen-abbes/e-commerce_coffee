from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order
from orders.models import OrderDetails
from .models import Payment
from django.utils import timezone #te3tik time 3la 7sab geography li tdekhelha 

# Create your views here.

def add_to_cart(request) :
    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous : #hado ga3 lil 7imaya kima rana char7in sabi9en
        pro_id = request.GET['pro_id'] #la valeur ta3 pro_id li hiya id ta3 product li drnaleh add to cart
        qty = request.GET['qty'] #la quantity li dekhelha utilisateur bach ydir add to cart
        #baghyin ndiro yla order is_finished ta3eh rah true y3ni user madatch odrer tsama ki had user ydir add to cart ynzad fog products li rah dayreh mn 9bel snn yla is_finished ra true tsama nefehmo beli had order jdid aya add to cart yenzad m3a order jdida 
        order = Order.objects.all().filter(user=request.user, is_finished = False)#order hada drnah bach net7e9o bih, user=request.user bach net2eko bli marahch anonymous is_finished = False ye3ni user mazal madarch a new order
        
        if not Product.objects.all().filter(id=pro_id).exists() : #if user ydekhel f lien(maybanch psq drnah b javascript lazem t3awed teketbeh) id ta3 Product ga3 mkach yretournih lel la page ta3 all products même ki tkon déconnecté tani
            return redirect('products')
        pro = Product.objects.get(id=pro_id)
        if order :
            #messages.success(request, 'There is an old order')
            old_order = Order.objects.get(user=request.user, is_finished = False)
            if OrderDetails.objects.all().filter(order=old_order, product=pro).exists() : #rah kan 3ndna prblm ki ndiro add to cart lel product w memb3ed nzido lnefs product ndiroleh add to cart ki nro7o lel cart nsibo dak product day 2 rows ta3 idafa lewla w zawja hna rana baghyin ki ydir add lnefs product nkheloh fi row wehda w nzido ghi quantity brk
                orderdetails = OrderDetails.objects.get(order=old_order, product=pro)
                orderdetails.quantity += int(qty) #qty = request.GET['qty'] 
                orderdetails.save()
            else :
                orderdeatils = OrderDetails.objects.create(product=pro, order=old_order, price=pro.price, quantity=qty)
            messages.success(request, 'Was add to cart for old order')
        else : #else tsama odrer jdid
            #messages.success(request, 'Here a new order will be done')
            new_order = Order() #drna object jdid psq 3ndna a new order
            new_order.user = request.user #n3emro les info ta3 user li dar biha login fl object jdid
            new_order.order_date = timezone.now() #nzidoleh la date
            new_order.is_finished = False #be3d ma kanet true ki drna order jdida reje3naha false w teg3od False hta user y3awed yechri mnjdid product machi ghi ydireh f sella brk, is_finished ykon True ghi min tkon Order jdida
            new_order.save() #drna save drwk howa lwl psq lazem new order ykon lawel bach ntigo nekhedo bl new order details psq mebni 3lih
            #hadi hiya haka ki nzido model jdid w nebgho n3emroh fl views ndiro had codes
            messages.success(request, 'Was add to cart for new order')
            orderdetails = OrderDetails.objects.create(product=pro, order = new_order, price = pro.price, quantity = qty) #hadi create 3emretelna fl table ta3 OrderDetails a new row li dekhelhom user, qty = request.GET['qty'] qty hiya name li fl input ta3 quantity 
        return redirect('/products/' + request.GET['pro_id']) #drna / 9bel bach yro7 direct lel products mayro7ch lel orders, tsama yedina lel product details li howa li drnaleh add to cart ye3ni ykhelik fnefs sef7a
    else : #else ykon déconnecté wla yekhreb fl url(yegle3 pro_id for example bsh pro_id w qty maghadich ybano psq fl product.html te7t ga3 f JavaScript rana dayrn mor maydir Confirm yesra submit li ydina l had fonction 
        #return redirect('products')
        if 'pro_id' in request.GET : #so if rah déconnecté w pro_id li hiya id ta3 product li dkhelna fih rah kayn 
            messages.error(request, 'You must be logged in')
            return redirect('/products/' + request.GET['pro_id'])
        else : 
            return redirect('index')


def cart(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous :
        if Order.objects.all().filter(user=request.user, is_finished=False) :
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.all().filter(order=order)
#hta lhna drna yla kan user dayr login w marahch anonymous w Order ta3h li darhom fl compte ta3h b1 sur w is finished rahi False so had orders ndirohm f whd variable smoh order w drna variable jdid orderdetails drna fih OrderDetails li ykon fiha order ta3ha égale order li créeenah megbila
            total = 0 #total hiya la somme total ta3 cha chra user wla cha saf f sella
            for sub in orderdetails : #orderdetails hiya variable li drnaha lfog
                total += sub.price * sub.quantity #total hiya variable mejmo3 ta3 prices * quantities li kaynin f fl variable orderdetails li kherejnaha lfog(hiya 3ibara 3en table)
                context={
                    'order' : order,
                    'orderdetails' : orderdetails,
                    'total' : total,
                }

    return render(request, 'orders/cart.html', context)



def remove_from_cart(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id :
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id :
            orderdetails.delete()
    return redirect('cart')    
    

def add_qty(request, orderdetails_id) : #hna ki tebghi t update quantity li tzidhom fl cart, hadi tzid quantity
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id :
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id :
            orderdetails.quantity +=1
            orderdetails.save()
    return redirect('cart')

def sub_qty(request, orderdetails_id) : #hadi tne9es quantity
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id :
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id :
            if orderdetails.quantity > 1 :
                orderdetails.quantity -=1
                orderdetails.save()
    return redirect('cart')



def payment(request):
    context = None
    ship_address = None
    ship_phone = None
    card_number = None
    expire = None
    security_code = None
    is_added = None
    if request.method == 'POST' and 'btnpayment' in request.POST  and 'ship_address' in request.POST and 'ship_phone' in request.POST and 'card_number' in request.POST and 'expire' in request.POST and 'security_code' in request.POST: #if ndiro submit f payment lazem ykon darek 3la submit mn button machi zayedha f lien, btnpayment name ta3 input ta3 submit ta3 Payment li fl payment.html
        #hna 3amaliyet def3 be3d deght 3la zir
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        card_number = request.POST['card_number']
        expire = request.POST['expire']
        security_code = request.POST['security_code']
        if request.user.is_authenticated and not request.user.is_anonymous : #hna t2eked bli rah authenticated w not anonymous
            if Order.objects.all().filter(user=request.user, is_finished=False) : #hna t2eked bli had user mazal makemel m3a order 9dima
                order = Order.objects.get(user=request.user, is_finished=False)
                payment = Payment(order=order, shipment_address=ship_address, shipment_phone=ship_phone, card_number=card_number, expire=expire, security_code=security_code)
                payment.save()
                order.is_finished = True #tsama order 9dima tro7
                order.save()
                is_added = True #9ader ma ndirohach nrml
                messages.success(request, 'Your order is finished')
        context = {
            'ship_address': ship_address,
            'ship_phone': ship_phone,
            'card_number': card_number,
            'expire': expire,
            'security_code': security_code,
            'is_added': is_added,
        }
    else :
        #hna l3erd 9bel al def3
        if request.user.is_authenticated and not request.user.is_anonymous : #hna t2eked bli rah authenticated w not anonymous
            if Order.objects.all().filter(user=request.user, is_finished=False) : #hna t2eked bli had user mazal makemel m3a order 9dima
                order = Order.objects.get(user=request.user, is_finished=False) #hna jab order b delala li t7e9e9 biha 9bel
                orderdetails = OrderDetails.objects.all().filter(order=order) #hn a jab orderdetails ta3 order li 9bel
    #hta lhna drna yla kan user dayr login w marahch anonymous w Order ta3h li darhom fl compte ta3h b1 sur w is finished rahi False so had orders ndirohm f whd variable smoh order w drna variable jdid orderdetails drna fih OrderDetails li ykon fiha order ta3ha égale order li créeenah megbila
                total = 0 #total hiya la somme total ta3 cha chra user wla cha saf f sella
                for sub in orderdetails : #orderdetails hiya variable li drnaha lfog
                    total += sub.price * sub.quantity #total hiya variable mejmo3 ta3 prices * quantities li kaynin f fl variable orderdetails li kherejnaha lfog(hiya 3ibara 3en table)
                    context={
                        'order' : order,
                        'orderdetails' : orderdetails,
                        'total' : total,
                    }
    return render(request, 'orders/payment.html', context)
#be3d ma dekhelna les infos fl payment page kherjetlna : Checkout Success : Your order is finished No Orders Here w ki ro7na lel Cart : No orders here All Products



def show_orders(request):
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous :
            all_orders = Order.objects.all().filter(user=request.user) #ga3 orderat ta3 user ki li chra ki li machrach psq rana baghyin ghi ne3erdohom
            if all_orders :
                for x in all_orders :
                    order = Order.objects.get(id=x.id) #hna kherejna ga3 orders li darhom user w 7etinahom fl order
                    orderdetails = OrderDetails.objects.all().filter(order=order)
        #hta lhna drna yla kan user dayr login w marahch anonymous w Order ta3h li darhom fl compte ta3h b1 sur w is finished rahi False so had orders ndirohm f whd variable smoh order w drna variable jdid orderdetails drna fih OrderDetails li ykon fiha order ta3ha égale order li créeenah megbila
                    total = 0 #total hiya la somme total ta3 cha chra user wla cha saf f sella
                    for sub in orderdetails : #orderdetails hiya variable li drnaha lfog
                        total += sub.price * sub.quantity
                    x.total = total
                    x.items_count = orderdetails.count
    context = {'all_orders' : all_orders}
    return render(request, 'orders/show_orders.html', context)


