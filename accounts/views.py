from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User #jebna User li mewjod f django par défault bach nzidoh m3a UserProfile
from django.contrib import auth #ghadi biha f signin
from .models import UserProfile #rana baghyin nsejlo lbayanat li ydekhelhom luser so nsejlo mn hadi addresse addr2 zip state city, wmel user nsejlo first name last name email password 
from products.models import Product
import re #regular expression bach net7e9o mel data li ydekhelha user f signup
# Create your views here.

def signin(request):
    if request.method == "POST" and "btnlogin" in request.POST: #if ndiro submit f signin, "btnlogin" in request.POST psq 9ader user yekhteb fl inspect w yem7i name ="btnlogin" wla yekhreb fiha aya drna hada chert bach ki yekhreb maytigch ysejel
        username = request.POST['user']
        password = request.POST['pass']
        user = auth.authenticate(username = username, password = password)#derna fih authentificate bach net7e9o mel username wel password bach ne3erfo yla howa nichan li dar signup wla la, username w password lwala ta3 data base ta3na ta3 User table w zawjin ta3 les variables li dernahom lfog yla rahom metsawyin tsama ta7a9o9 s7i7
        if user is not None : #if user fih 7aja mrahch None
            if "rememberme" not in request.POST : #if user ki ydir login ma ydirch check 3la remember me
                request.session.set_expiry(0) #ki ybele3 lbrowser w y3awed y7eleh lazem y3awed ydekhel username w password bach ydir login
            auth.login(request, user) #hna tkeli golnaleh dir login
            #messages.success(request, "You are now logged in")
        else :
            messages.error(request, "Username or passwoed invalid")
        #moraha drna loggout w ki dekhelna username w password ghaltin kherjetlna Error : Username or passwoed invalid
        #moraha 3awed dekhelna username w password nichan affichalna Success : You are now logged in
        #bach n2ekdo beli nta nichan dert loggin ro7na lel la page http://127.0.0.1:8000/admin kherjetlna You are authenticated as wael, but are not authorized to access this page. Would you like to login to a different account? me3netha wael machi messala7iyat taw3eh yedkhol la page admin psq mahoch mn stuff users member nrml f site bsh machi admin
        return redirect('signin')
    else : #hadi faydetha ga3 ki tebghi tzid tkhreb f lien w tzid kach link moraha http://127.0.0.1:8000/accounts/signin?... aya yeg3od ghi kima rah 
        return render(request, "accounts/signin.html")
    
def logout(request):
    if request.user.is_authenticated : #if user rah dayer login tsema ynejem ydir logout
        auth.logout(request) #tsama bhadi ydir logout
    return redirect("index")
def signup(request):
    if request.method == "POST" and "btnsignup" in request.POST: #if ndiro submit f signin lazem ykon darek 3la submit mn button machi zayedha f lien
        #Variables for fields
        fname = None
        lname = None
        address = None 
        address2 = None
        city = None
        state = None
        zip_number = None
        email = None
        username = None
        password = None
        terms = None #ta3 checkbox hadi li tji te7t
        is_added = None
        #get values from the form
        if "fname" in request.POST : #fname hiya name li rahi fl input, hna n9sdo if user dakhel data fl input
            fname = request.POST['fname'] #fname hiya name li rahi fl input ta3 the first name fl form signup.html
        else : # hna machi me3netha kheliteh khawi linput psq kon tkheliha khawya men 3ndhom ygolek lazem t3emer input bsif, drnaha lel 7imaya psq 9ader user yekhreb w ydrir inspecter lel la page w ybedel name ytig ydir signup bla ma ydekhel username par exmpl, psq lfog drna if "fname"
            messages.error(request, 'error in first name')
        if "lname" in request.POST : 
            lname = request.POST['lname']
        else : 
            messages.error(request, 'error in last name')
        if "address" in request.POST :
            address = request.POST['address']
        else : 
            messages.error(request, 'error in address')
        if "address2" in request.POST :
            address2 = request.POST['address2']
        else : 
            messages.error(request, 'error in address 2')
        if "city" in request.POST :
            city = request.POST['city']
        else : 
            messages.error(request, 'error in city')
        if "state" in request.POST :
            state = request.POST['state']
        else : 
            messages.error(request, 'error in state')
        if "zip" in request.POST :
            zip_number = request.POST['zip']
        else : 
            messages.error(request, 'error in zip')
        if "email" in request.POST :
            email = request.POST['email']
        else : 
            messages.error(request, 'error in email')
        if "user" in request.POST :
            username = request.POST['user']
        else : 
            messages.error(request, 'error in username')
        if "pass" in request.POST :
            password = request.POST['pass']
        else : 
            messages.error(request, 'error in password')
        if "terms" in request.POST :
            terms = request.POST['terms']
        
        #Check the values :
        if fname and lname and address and address2 and city and state and zip_number and email and username and password : #tsama if machi None 
            if terms == "on": #if user dar checkbox me3naha sade9 3la 9awanin site
                #Check if the username is taken ze3ma yla khadmin bih mn 9bel
                if User.objects.filter(username = username).exists() : #if ta3 username li dekhleh lmostakhdim kayen déjà fl filter li drnah fl username ta3 User
                    messages.error(request, "This username is taken") #golnaleh had username dayrinh mn 9bel dir whd unique
                else :
                    #Check if the email is taken
                    if User.objects.filter(email = email).exists():
                        messages.error(request, "This email is taken")
                    else :
                        patt = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                        if re.match(patt, email) : #if regular expression patt motabi9 m3a email
                            #Add user, jedwel lawel li kayn f django par défault
                            user = User.objects.create_user(first_name=fname, last_name = lname, email = email, username = username, password=password) #create_user django dayerha même les variables dakhel al a9was kima create_user create_user ta3 django, hna segemna brk l7o9ol w data li dakhelha user mn la page dernaha fl user
                            user.save() 
                            #add user profile, hna zedna table lfer3i ta3 UserProfile, tsma lazem ndiro save lel table al assassi User howa lawel memb3ed lfer3i haka tkhdm data base
                            userprofile = UserProfile(user = user, address = address, address2 = address2, city = city, state = state, zip_number = zip_number) #user lawel représente attribute li rah fl UserProfile w user zawej dakhel l9ews howa li rah lfog address lwl ta3 UserProfile zawj ta3 lfog wa hakada drnah bach yerbetlna table User m3a UserProfile
                            userprofile.save()
                            #clear fields, ki ndekhel me3lomat ta3i nichan f signup w yekhrejli msg success w yesra render lnefs la page li rani fiha mes infos li sejelt bihom yego3do dahrin so hna rani baghi nem7ihom yege3do dahrin sauf yla kayn error fl data li ydekhlha user bach y3awed yse7e7hom 
                            fname = ""
                            lname=""
                            address = ""
                            address2 = ""
                            city=""
                            state=""
                            zip_number=""
                            email=""
                            username=""
                            password=""
                            terms=None
                            #Success message, hna ki ndekhlo les informations nichan w nsad9o 3la terms tekhrejlna success w f la page admin tani yenzad user jdid soit f table User wla UserProfile
                            messages.success(request, "Your accounte is created")
                            is_added=True #tkon true ki yedhe msg success li lfog
                        else :
                            messages.error(request, "Invalid email")
            else :
                messages.error(request, "You must agree to the terms")
        else :
            messages.error(request, 'Check Empty Fields')
            #konna ki ndiro submit w ndekhlo me3loma ghalta ki ndiro signup yekhrejln msg error aya w la page yesralha reload bsh les infos li kona mdekhlinhom yro7o ga3 rana baghyin nkhelohom ghi kima rahom w user ysegemhom so ghadi nfewto context te7t, moraha nro7o lel la signup.html w nzido dok contexts fl inputs exactly fl value
        return render(request, 'accounts/signup.html',{
            'fname':fname, 'lname':lname, 'address':address, 'address2':address2, 'city':city, 'state':state, 'zip':zip_number, 'email':email, 'user':username, 'pass':password, 'is_added':is_added
        }) 
    else :
        return render(request, 'accounts/signup.html')

def profile(request):
    if request.method == "POST" and "btnsave" in request.POST: #if ndiro submit f la page ta3 profile
        if request.user is not None and request.user.id != None : ##if user rah dayer signin nichan, (kima glna anonym li user.id = None 3adha not None), if marahch anonymous ye3ni if rah dayer login, 
            #naghyin n3edlo fl bayanat lfer3iya li hiya ta3 model UserProfile
            userprofile = UserProfile.objects.get(user=request.user) #glnaleh dir fl user li fl model ta3 UserProfile data ta3 request.user li dekhelha user ki dar modifier lel compte fl la page ta3 profile donc userprofile wlat fiha ga3 les attributs ta3 UserProfile 
            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['city'] and request.POST['state'] and request.POST['zip'] and request.POST['email'] and request.POST['user'] and request.POST['pass']:#drnaha bach yla khreb user fl form ma yesrach submit
                request.user.first_name = request.POST['fname'] #first_name attribute wajda fl model ta3 User fl django da la valeur ta3 fname li dekhelha user ki dar modifier fl la page ta3 profile, user hada li rbetna bih fl model UserProfile nejmo nkherjo mneh les attributs ta3 User w UserProfile chghol wassit
                request.user.last_name = request.POST['lname'] 
                userprofile.address = request.POST['address'] #hada ta3 table zawej UserProfile 
                userprofile.address2 = request.POST['address2']
                userprofile.city = request.POST['city']
                userprofile.state = request.POST['state']
                userprofile.zip_number = request.POST['zip']
                #request.user.email = request.POST['email'] #gl3nahom psq kon drnahom 9ader user yekhreb fl value w ybedel email
                #request.user.username = request.POST['user']
                #be3d ma tebetna les valeurs f User w UserProfile drwk ndirolhom save
                request.user.password = request.POST['pass']
                if not request.POST['pass'].startswith('pbkdf2_sha256$') : #f la page ta3 profile password est crypté, ki dkhelna lel pgadmin tables->auth_user->right click->Edit data/view->all rows tema tsib password lcrypté ta3k ta3 chaque user w ga3 tsibhom badyon b pbkdf2_sha256$so hadi li drnaha dakhel al9ews,kon tro7 lel la page profile tsiba fl input ta3 password m3emra hadak rah mot de passe crypté, so if password li dekhleh user fl profile yebda b hadik li dakhel al9ews tsama user ma bedel walo madekhel password ma walo khalaha kimarahi w hadak password crypté kan 9ader yro7 lel database as a new password bsh hn rana dayrin if not tsam if paswword mayebdach b hadok li dakhel al9ews a tsama hna rah mdekhel a new password machi pawwsprd crypté khelah kima rah
                    request.user.set_password(request.POST['pass']) #drna save lel password jdid li modiefah user fl la page profile
                request.user.save() #save lel bayanat ta3 model User li dekhelnahom fl la page profile
                userprofile.save()  #save lel bayanat ta3 model UserProfile li dekhelnahom fl la page profile
                auth.login(request, request.user) #hna ydir login psq kon mandirohach user ki ydir changes lel profile ydéconnécta so ndiro hadi bach yeg3od connecté fl la page profile  
                messages.success(request, 'Your data has been saved')
            else :
                messages.error(request, 'Check your values and elements')
        return redirect('profile')
    else : #dkhel bla ma ydir submit ça se peut ykon dkhelha men kach lien wla
        #if request.user.is_anonymous : return redirect('index') #if yedkhol utilisateir lel profile bma maydir signin tsama rah anonymous
        #if request.user.id == None : return redirect('index') #kifkif m3a lfoganiya ki ykon id ta3 utilisateur None tsama rah anonymous w baghi yedkhol 3la la page ta3 profile
        
        if request.user is not None : #if user rah dayer signin nichan
            #if request.user.is_anonymous : return redirect('index') #hna user anonymous rah me3dod not None
            #if request.user.is_anonymous : return redirect('index') #hna user anonymous rah me3dod None w marahch yekhdem ki dtna run lel la page
            #if request.user.is_anonymous : #error anonymous
            context = None
            if not request.user.is_anonymous : #(kima glna anonym 3adha not None), if marahch anonymous ye3ni if rah dayer login yaffichi la page ta3 profile nrml snn yaffichilina You must be logged in, (9ader ndiro if request.user.id == None kifkif)
                userprofile = UserProfile.objects.get(user=request.user)#userprofile ntigo nkherjo mnha ga3 data ta3 utilisateur li rahi fl UserProfile, golnaleh get bime3na jib bidalalet user li fl model ta3 UserProfile li rbetelna bin had model w bin ta3 User b OneToOnefield dernah bach yedbetelna les attributs ta3 UserProfile 3la 7sab ta3 User psq user hada howa foreign key so khdemna bih bach kol les attributs ta3 User y9ablo ta3 UserProfile bitari9a sa7i7a
                context = { #hna n3emro les inputs li fl la page ta3 profile b les infos ta3 user mn model ta3 django User w mn model ta3 UserProfile bach ymodifier 3lihom teshal 3lih
                    "fname": request.user.first_name, #first_name représente name li fl input fl html
                    "lname": request.user.last_name,
                    "address": userprofile.address,
                    "address2": userprofile.address2,
                    "city": userprofile.city,
                    "state": userprofile.state,
                    "zip": userprofile.zip_number,
                    "email": request.user.email,
                    "user": request.user.username,
                    "pass": request.user.password,
                            }
            return render(request, 'accounts/profile.html', context)
        else :
            return redirect('profile')


def product_favorite(request, pro_id): #pro_id hna kima drna fl product details hadi drnaha psq fl lien mor product/ ghadi nzido product_favorite/ moraha number yindiquer 3la le id(nombre) ta3 product li rana dakhlin fih fl favorite 
    if request.user.is_authenticated and not request.user.is_anonymous : #if user rah dayer login
        pro_fav = Product.objects.get(pk=pro_id) #kima ne3erfo f database f pgAdmin products ga3 mre9min bl id(pro_id) kima hna golnaleh jibelna ga3 Product bidalalet id tawe3hom w 7atinahom fl pro_fav
        #django mekhdom ki neclicko 3la favorite (dik nejma) tebda ghi tendaf f data base so lewla net2ekdo beli user marahch dayer favorite mn 9bel bach ki yeclicki user fl fav tendaf ghi khetra
        if UserProfile.objects.filter(user=request.user, product_favorites=pro_fav).exists() : #golnaleh dir if rah kayen filter 3la user fl UserProfile rah yossawi request li dekhelha l user ki dar authenticated(login) w UserProfile ki ykon product_favorites li rbetna bih bin UserProfile w Product(many to many) yossawi pro_fav li fih ga3 Product bidalalet les id tawe3hom, tsama hna user dar idafa lel product hna fl favorite
            #tsama bikhtissar lfog han golnaleh if rah kayn utilisateur sejel b compte rah fl User w product_favorites rah mendaf fih des produits mn Product
            messages.success(request, 'Already product in the favorite list') #aya hna ngololeh sayi hada product rah mendaf mn 9bel
        else : #yla hada product marahch mendaf aya ndifoh
            userprofile = UserProfile.objects.get(user=request.user) #golnaleh jiblena UserProfile biha b les attributs ta3 ki ykon user li fl UserProfile howa request.user ye3ni howa user li rah logged
            userprofile.product_favorites.add(pro_fav) #cbn hna dfna fl UserProfile.product_favorites product jdid li id ta3eh pro_id
            messages.success(request, 'Product has been favorited') #w drnaleh msg bli tem idafet product
        
#user ki yekhol f a product w ydireh favorisé url yersel pro_id li howa id ta3 had produt lel views exactly tro7 3nd la fonction product_favorite w ydir te7a9o9 yla product li rah dakhel fih user(pro_fav) rah kayen fl table ta3 product_favorites yerseleh msg bli cbn rak dayer fav mn 9bel snn yzid had product li darleh favorisé lel product_favorites w yaffichi msg bli sayi product dertleh fav
    else : #if marahch dayr login ye3tina msg error
        messages.error(request, 'You must be logged in')
    return redirect('/products/' + str(pro_id)) #hna golnaleh ro7 lel Product Details drna / 9bel products bach yefhem beli products rah jay min aslo psq kon mandirohach ye7seb golnaleh ro7 lel accounts/products psq rana fl accounts, pro_id drnah f str psq howa integer bach ytig ndiroleh concatination, so te3tina products/pro_id


def show_product_favorite(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous : #if user rah dayer login
        userInfo = UserProfile.objects.get(user=request.user) #hna jebna objects ta3 UserProfile ta3 utilisateur li rah dayr login
        pro = userInfo.product_favorites.all() #hna kherejna product_favorites ta3 dak utilisateur
        context = {'products':pro} #drwk products représente pro fl html
    return render(request, 'products/products.html', context) #yedina lel la page ta3 products w yaffichilna ghi favorites products
