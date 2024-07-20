from django.db import models
from django.contrib.auth.models import User #drna import lel model(table) ta3 User li fl django par défault b1 sûr
from products.models import Product #bayna 3ayetna lel model ta3 Product ml app ta3 products
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

# Create your models here.

#ghadi ndiro order howa lwl psq order details yedi id ta3 order 3labiha lazem tndar lwla
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)#hna bi nerbto m3a User psq glna bli kayn relation one to many bin User w order 3labiha drna id User yro7 as a foreignkey lel order
    order_date = models.DateTimeField() #la date li dar fiha order
    details = models.ManyToManyField(Product, through = 'OrderDetails')#kima golna bli kayna relation many to many bin Order w Product so drna table wassit binathom(through) li howa OrderDetails ,hadi ghadi terbet bin Order w bin order details li ghadi memb3ed ndiro te7t
    is_finished = models.BooleanField() #True or False esq utlisateur tleb order hada wla ghi 7eteh f sella brk bla maydir order(bla ma yechri), par défault True
    total = 0 #hado drnahom m3a tali bach ne7esbo bihom 9ader n3eytolhom win ma bghina soit fl views wla templates
    items_count = 0
    def __str__(self):
        return 'User: ' + self.user.username + ', Order id: ' + str(self.id) #tetafficha f datebase User: username, order id: order_id bach mayesrach tikrar f username, id django ydireh we7deh bla ma ndiroh as an attribute
    
class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)#hna bi nerbto m3a Product psq glna bli kayn relation one to many bin Product w OrderDetails 3labiha drna id Product yro7 as a foreignkey lel OrderDetails
    order = models.ForeignKey(Order, on_delete=models.CASCADE)#hna bi nerbto m3a Order psq glna bli kayn relation one to many bin Order w OrderDetails 3labiha drna id Order yro7 as a foreignkey lel OrderDetails
    price = models.DecimalField(max_digits=6, decimal_places = 2) #max_digits représente a9sa 3adad khanat ta3 prix ta3 products taw3k hna rana dayrin 6 tsama mayfotch 999999, ah 7rez hna rana dayrin decimal_places=2  me3netha 6 khanat, 2 men hadok 6 khanat fassila tsama a9sa prix 9999.99, tkheyel nta rah 3ndk product fl site w chraw mneh ch7al mn imagine rmemb3ed price ta3 hadak product yzid drwk prices l9dem li charyinhom users mn 9bel w rahom f database yetbedlo tsma hna tsra karita l7sab ta3 mabi3at taw3ek ga3 ywelo ghaltin, so hada li khelana n7eto price hna bach yetenregistra 3ndek w mayetbedelch
    quantity = models.IntegerField()
    def __str__(self):
        return 'User: ' + self.order.user.username + ', Product: ' + self.product.name + ', Order id: ' + str(self.order.id)

    def Meta(): #drnaha bach ki ydir user update lel quantity(add or sub) yerje3 ga3 tali
        ordering = ['-id']

    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) #drna order psq bih ntigo neweslo lel user w orderdetails, hna drna id ta3 Order yro7 as foreign key 3nd Payment tsama one to many order whda dir chhal mn payment
    shipment_address = models.CharField(max_length=150)
    shipment_phone = models.CharField(max_length=50)
    card_number = CardNumberField()
    expire = CardExpiryField()
    security_code = SecurityCodeField()

    

