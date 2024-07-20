from django.db import models
from datetime import datetime

# Create your models here.
class Product(models.Model) :
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places = 2) #max_digits représente a9sa 3adad khanat ta3 prix ta3 products taw3k hna rana dayrin 6 tsama mayfotch 999999, ah 7rez hna rana dayrin decimal_places=2  me3netha 6 khanat, 2 men hadok 6 khanat fassila tsama a9sa prix 9999.99
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/') #upload_to tdirli folder bism photos ydir fiha folder bism l3am li tecréat fiha w ydir fiha dakhel l3am folder ta3 month w dakhel lmonth folder ta3 day li tecréa plutôt li tele3na fiha fiha photo wyzid lphoto tani f database ta3 LI FL pgAdmin
    is_active = models.BooleanField( default=True ) #hna ki ndif prodyct yetmarka True drct
    publish_date = models.DateTimeField( default=datetime.now) #la date li defna fiha product, la date par défault hiya la date ta3 li tebghi dif fiha lproduct
    def __str__(self):  #lproduct yetaficha f db b name ta3h
        return self.name
    
    class Meta : #binretbo products mel a7det lel a9dem
        ordering = ['publish_date']  #publish_date howa ism l7e9l li nretbo bih, haka ye3tina product li defnah le plus récente howa li yetafficha lewel, ['-publish_date'] l3eks li difeh yetafficha howa tali te7t ga3