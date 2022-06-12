from django.contrib import messages,auth
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from requests import Response
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .forms import OrderForm
from django.core.mail import EmailMultiAlternatives
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
import csv
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from Accounts.forms import UserprofileForm
# Create your views here.
def home(request):
    itineraries = Itinerarie.objects.raw("select * from ItineraryAppManagement_Itinerarie order by random() limit 8")
    itinerary = Itinerarie.objects.raw("select * from ItineraryAppManagement_Itinerarie order by random() limit 8")
    continents=Continent.objects.all()
    countries=Country.objects.all()
    city=City.objects.all()
    banner=Banner.objects.all()
    itinerary_images = Itinerariesimage.objects.all()
    context={
        'all':itineraries,
        'top':itinerary,
        'continents':continents,
        'countries':countries,
        'city':city,
        'banner':banner,
        'image':itinerary_images,
    }
    return render(request, 'index.html',context)

def newsletter(request):
    if request.method=="POST":
        email=request.POST.get('email')
        data=Newsletter(email=email)
        messages.success(request,'Thanks for subscribing our newsletter!')
        data.save()
        return redirect('home')
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')

@login_required(login_url="login")
def dashboard(request):
    order = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered = True)
    orders_count = order.count()
    context = {
        'orders_count': orders_count,
        'order':order,
    }
    return render(request, 'dashboard.html', context)
    

@login_required(login_url="login")
def checkout(request,total=0,cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total=total+(cart_item.product.price)
            print(total)

    except ObjectDoesNotExist:
        pass #just ignore
    context = {
        'cart_items': cart_items,
        'total':total,
       }

    return render(request,"checkout.html",context)



def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            itinery=Itinerarie.objects.filter(Q(country__country_name__icontains=keyword)|Q(continent__continent_name__icontains=keyword)|Q(state__city_name__icontains=keyword)|Q(small_description__icontains=keyword)|Q(name__icontains=keyword))
            related_iti = Itinerarie.objects.filter(Q(country__country_name__icontains=keyword)|Q(continent__continent_name__icontains=keyword)|Q(state__city_name__icontains=keyword))
        context={
        "itinery":itinery,
        "related_iti":related_iti
        }  
    return render(request,'itenararies.html',context) 
    
def itinerary(request,country_slug=None,city_slug=None):
    continents=Continent.objects.all()
    all_countries=Country.objects.all()
    city=City.objects.all()
        
    if country_slug!=None and city_slug==None:
        countries=get_object_or_404(Country,country_slug=country_slug)
        itinery=Itinerarie.objects.filter(country=countries) 
        related_iti =  Itinerarie.objects.filter(country=countries)
        print(itinerary)
    elif country_slug!=None and city_slug!=None:
        countries=get_object_or_404(Country,country_slug=country_slug)
        cityslug=get_object_or_404(City,slug=city_slug)
        itinery=Itinerarie.objects.filter(country=countries,state=cityslug)
        related_iti =  Itinerarie.objects.filter(country=countries,state=cityslug)  
        print(itinerary)
    else:
        itinery=Itinerarie.objects.all()
    context={
        "itinery":itinery,
        "related_iti":related_iti,
        "continents":continents,
        "all_countries":all_countries,
        "city":city,
    }
    return render(request,'itenararies.html',context)   

def itinerary_details(request,country_slug,itineraries_slug):
    single_product=Itinerarie.objects.get(country__country_slug=country_slug,slug=itineraries_slug)
    itinerary_images = Itinerariesimage.objects.all()
    context={
        "single_product":single_product,
        'image':itinerary_images,
    }
    return render(request,'itinerary_detail.html',context)


def customized_itinerary(request):
    states = City.objects.all()
    country=Country.objects.all()
    continent=Continent.objects.all()
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        mobile=request.POST.get("mobile")
        name_itinerary=request.POST.get("name_itinerary")
        state=request.POST.get("state")
        country=request.POST.get("country")
        continent=request.POST.get("continent")
        budget=request.POST.get("budget")
        day=request.POST.get("day")
        night=request.POST.get("night")
        no_of_adults=request.POST.get("no_of_adults")
        no_of_childs=request.POST.get("no_of_childs")
        from_date=request.POST.get("from_date")
        to_date=request.POST.get("to_date")
        vacation=request.POST.get("vacation")
        info=request.POST.get("info")
        data=Customized_Itinerary(name=name,email=email,mobile=mobile,name_itinerary=name_itinerary,state=state,country=country,continent=continent,budget=budget,day=day,night=night,no_of_adults=no_of_adults,no_of_childs=no_of_childs,from_date=from_date,to_date=to_date,vacation=vacation,info=info)
        data.save()
        messages.success(request,"we've got your cutomized Itinerary we will contact you soon")
        return redirect('home')
    return render(request, 'customized_itinerary.html',{'states':states,'country':country,'continent':continent})

def added_cart(request,product_id):
    url = request.META.get('HTTP_REFERER')
    current_user=request.user
    product=Itinerarie.objects.get(id=product_id)
    if current_user.is_authenticated:
        is_cart_item_exists=CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user=current_user)
            messages.success(request,'Your itinerary already added to cart')
        else:
            cart_item=CartItem.objects.create(
            product=product,
            user=current_user,
            )
            messages.success(request,'Your itinerary added to cart')
            cart_item.save()
        return redirect(url)

    else:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            
        except Cart.DoesNotExist:
                cart=Cart.objects.create(
                    cart_id=_cart_id(request)
                )
        cart.save()
        is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
                cart_item=CartItem.objects.filter(product=product,cart=cart)
                
        else:
                cart_item=CartItem.objects.create(
                product=product,
                cart=cart,
                )
                cart_item.save()
        return redirect(url)   


def my_profile(request):
    if request.method=="POST":
        email=request.POST.get('email')
        data=Newsletter(email=email)
        data.save()
        return redirect('home')    
    return render(request, 'my_profile.html')


def _cart_id(request):
    cart=request.session.session_key
  
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Itinerarie.objects.get(id=product_id) #get the product
    cart_id = _cart_id
    # If the user is authenticated
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
        else:
            CartItem.objects.create(
                product = product,
                user = current_user,
            )

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                )
            cart.save()
        return redirect('cart')

def cart(request,total=0,cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
            
        for cart_item in cart_items:
            total=total+(cart_item.product.price)
    except ObjectDoesNotExist:
        pass

    context={
            'cart_items':cart_items,
            'total':total,
            }      
    return render(request,'cart.html',context)

def remove_cart_item(request,product_id,cart_item_id):
    
    product=get_object_or_404(Itinerarie,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(user=request.user,product=product,id=cart_item_id)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_item_id)  

    except:
            pass
    cart_item.delete()

    return redirect('cart')  


@login_required(login_url="login")
def place_order(request,total=0):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('home')
    grand_total=0
    tax=0

    for cart_item in cart_items:
        total=total+(cart_item.product.price) 
    tax=(8*total)/100
    grand_total=total+tax
    
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.email=form.cleaned_data['email']
            data.phone=form.cleaned_data['phone']
            data.countryphone_code=form.cleaned_data['countryphone_code']

            data.tax=tax
            data.order_total=grand_total
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'payments.html',context)
        else:
            return HttpResponse('if not working')
    else:
        return redirect('checkout')
        

        
            

@login_required(login_url="login")
def payments(request):
    return render(request,'payments.html')

def razorpay(request,id):
    import razorpay
    order_details = Order.objects.get(id=id)
    client = razorpay.Client(auth=("rzp_test_B9st9Hrr0Tp8ZA", "Ve68z22EhYIf3jOBrBo3o8Th"))
    data = { "amount": int(order_details.order_total)*100, "currency": "INR", "receipt": "Itinerary Buddy" }
    payment_amount=data["amount"]
    payment = client.order.create(data=data)
    razorpay_order_ID = payment['id']
    amount = data.get('amount')
    name = {order_details.email}

    payment  = Payment(
    user=request.user,
    payment_id=razorpay_order_ID,
    amount_paid=order_details.order_total,
    status=True,
    created_at=datetime.datetime.now
    )
    payment.save()

    order=Order.objects.get(user=request.user,is_ordered=False,id=order_details.id)
    order.payment=payment
    order.save()

    cart_items=CartItem.objects.filter(user=request.user)
   
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product_id
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()

        orderproduct=OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.save()

    CartItem.objects.filter(user=request.user).delete()
    context = {'amount':amount,'name':name,'razorpay_order_ID':razorpay_order_ID,'order_details':order_details}
    return render(request,"razorpay.html",context)

def payment_done(request,id):
    order=Order.objects.filter(id=id).update(is_ordered=True)
    return render(request,'payment_success.html')




def profile(request, id):
    url = request.META.get('HTTP_REFERER')
    userprofile=get_object_or_404(Account,id=id)
    if request.method=='POST':
        profile_form=UserprofileForm(request.POST or None, request.FILES or None,instance=userprofile)
        if profile_form.is_valid():
            obj = profile_form.save(commit=False)
            obj.save()
            messages.success(request,"Your profile has been updated")
            userprofile = obj
            return redirect(url)
    profile_form = UserprofileForm(initial = {
        "username": userprofile.username,
        "email": userprofile.email,
        "mobile": userprofile.mobile,
        "nationality": userprofile.nationality,
        "country": userprofile.country,
        "profile_pic": userprofile.profile_pic,
    })
    context={
          'profile_form':profile_form,
          'userprofile':userprofile,
    }
    return render(request, 'profile.html',context)

@csrf_exempt
def send_message(request):
    url = request.META.get('HTTP_REFERER')
    if request.method=="POST":
        email=request.POST.get("email")
        mail_subject =request.POST.get('subject')
        emailmessage=request.POST.get("message")
        username=request.POST.get("name")
        print(email,emailmessage,mail_subject,username)
        current_site=get_current_site(request)#current site ko fetch krega
        
        user = username
        html_message=emailmessage        
        to_email=email
        html_body=render_to_string('mailing.html',{'user':user,'domain':current_site,'message':html_message,})

        send_mail = EmailMultiAlternatives(
        subject=mail_subject,
        body=emailmessage,
        to=[to_email]
        )
        # send_mail=EmailMessage(mail_subject,message,to=[to_email])#list me h for more than one users
        send_mail.attach_alternative(html_body, "text/html")
        send_mail.send(fail_silently=False)
        msg = messages.success(request,"Mail Send Successfully ")
        return HttpResponse("Mail Sended Successfully")

def render_pdf_view(request,id):
    order=OrderProduct.objects.filter(order=id)
    template_path = 'invoice_pdf.html'
    context = {"order":order}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ItineraryInvoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response )
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_view_itinerary(request,id):
    order=OrderProduct.objects.filter(order=id)
    itinerary_images = Itinerariesimage.objects.all()

    template_path = 'itinerary_pdf.html'
    context = {"order":order,"image":itinerary_images}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ItineraryDetail.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response )
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

