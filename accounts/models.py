from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class UserProfile(models.Model): #psq ki ykon 3ndna une relation one to one kima hna bin User W UserProfile ndiro id ta3 User li sminah user fl UserProfile as FOREIGN KAY,derna had lmodel psq hna 3ndna user f bdd mafihch address w addree2 zip(code postal)... aya rana baghyin ndiro had lmodel w nzidoh w nrebtohom m3a les infos ta3 user kon mayjonch les infos maykonch hna
    user = models.OneToOneField(User, on_delete = models.CASCADE) #dina copy mel User
    product_favorites = models.ManyToManyField(Product)#hna rbetna bin UserProfile w Product many to many so product_favorites rah wassit bin les deux tables, moraha ndiro migrate as usual ki nro7o lel pgAdmin w ndiro refresh 3la public nchofo bli zadelna table jdid smoh acoount_userprofile_product_favorites fih id ta3h w ta3  UserProfile w ta3 Product psq hada rah ymetel wassit ki ykon 3ndna many to many yendar fih les id ta3 les deux tables as foreignkeys
    address = models.CharField(max_length=60)
    address2 = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    zip_number = models.CharField(max_length=5)

    def __str__(self):
        return self.user.username #jbna username men user 