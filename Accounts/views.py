
from django.shortcuts import render,redirect
from regex import E
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from ItineraryAppManagement.models import Cart,CartItem
from django.contrib.auth.tokens import default_token_generator
from ItineraryAppManagement.views import _cart_id
import json

# Create your views here.
#user->pk=1->uid=1234->token=34@As->email->link->htmlfile->decode hoga email->is active true hoga



def register(request):
    form=RegistrationForm(request.POST)
    try:
        if request.method=="POST":
            print('resq is post')
            if form.is_valid():
                print('form is valid')
                username=form.cleaned_data["username"]
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                clientkey = request.POST['g-recaptcha-response']
                secretkey = '6LdDi_gfAAAAAIxA2fHX72xJ_Y3NYg3J1-1l3QA5'
                captchtadata ={
                    'secret':secretkey,
                    'response':clientkey,
                }
                r= request.post('https://www.google.com/recaptcha/api/siteverify',data=captchtadata)
                response=json.loads(r.text)
                verify=response["succes"]
                print("your success is",verify)
                user=Account.objects.create_user(username=username,email=email,password=password)
                user.save()            
                current_site=get_current_site(request)#current site ko fetch krega
                mail_subject="Please activate your account"
                message=render_to_string('account_verification_email.html',{
                        'user':user,
                        'domain':current_site,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),#jo user save hora uska primary key save krega
                        'token':default_token_generator.make_token(user),

                    })
                to_email=email
                send_mail=EmailMessage(mail_subject,message,to=[to_email])#list me h for more than one users
                send_mail.send()
                messages.success(request,"Registration Successful")
                return redirect('home')
            else:        
                form=RegistrationForm()
    except:
        messages.error(request,"Captcha didn't matched try it again")
        return redirect('register')        
    context={
        'form':form
    }
    return render(request,"register.html",context)


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulations your account is activated")
        return redirect('login')
    else:
        messages.error(request,"Invaild Activation Link")
        return redirect('register')
        
def login(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    # cart_item=CartItem.objects.filter(user=user)
                    for item in cart_item:
                        print(item)
                        item.user=user
                        item.save()
            except:
                pass

            auth.login(request,user)
            messages.success(request,'You have been successfully logged in')
            return redirect('home')
        else:
            messages.error(request,"Invaild login credentials")
            return redirect('login')
    return render(request,'login.html')



@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

def forgotpassword(request):
    if request.method=="POST":
       email=request.POST["email"]
       if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="Reset Your Password"
            message=render_to_string('reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])#list me h for more than one users
            send_mail.send()
            messages.success(request,"An Email has been sent to Reset your Password")
            return redirect('login')
       else:
           messages.error(request,"Account does not exist")
           return redirect('login')
        
    return render(request,"forgotpassword.html")

def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,"please reset your password")
        return redirect('resetpassword')
    else:
        messages.error(request,"The Link has expired")
        return redirect('login')
    

def resetpassword(request):
    if request.method=="POST":
        password=request.POST["newpassword"]
        confirmpassword=request.POST["confirmpassword"]
        if password==confirmpassword:
           uid= request.session.get('uid')
           user=Account.objects.get(pk=uid)
           user.set_password(password)
           user.save()
           messages.success(request,"password reset successfully")
           return redirect("login")
        else:
            messages.error(request,"password does not match")
            return redirect('resetpassword')
    return render(request,"resetpassword.html")


@login_required(login_url="login")
def change_password(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        
        user=Account.objects.get(username=request.user.username)
        
        if new_password==confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,"Your password has been changed")
                return redirect('change_password')
            else:
                messages.error(request,"please enter valid password")
                return redirect('change_password')
        else:
             messages.error(request,"password doesnot match")
             return redirect('change_password')
            
    
    return render(request,"change_password.html")
