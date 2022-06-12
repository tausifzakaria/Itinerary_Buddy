from pickle import TRUE
from turtle import title
from django.db import models
from django.urls import reverse
from Accounts.models import Account
from django.utils.safestring import mark_safe
from tinymce.models import HTMLField
from phonenumber_field.modelfields import PhoneNumberField

class Continent(models.Model):
    continent_name = models.CharField(max_length=50)
    continent_slug = models.SlugField()
    continent_code = models.CharField(max_length=10)
    def __str__(self):
        return self.continent_name

class Country(models.Model):
    country_name = models.CharField(max_length=50)	
    country_slug = models.SlugField()
    country_code = models.CharField(max_length=10)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    def __str__(self):
        return self.country_name
    def get_url_country(self):
        return reverse("country_detail",args=[self.country_slug])


class City(models.Model):
    city_name = models.CharField(max_length=50)
    slug = models.SlugField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    def __str__(self):
        return self.city_name

    def get_url_city(self):
        return reverse("city_detail",args=[self.country.country_slug,self.slug])

class Itinerarie(models.Model):
    RATING=(
        ('0.5','0.5'),
        ('1','1'),
        ('1.5','1.5'),
        ('2','2'),
        ('2.5','2.5'),
        ('3','3'),
        ('3.5','3.5'),
        ('4','4'),
        ('4.5','4.5'),
        ('5','5'),
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    price = models.IntegerField()
    package = models.CharField(max_length=50, default="5 Days|2 Night")
    currency_code = models.CharField(max_length=5)
    small_description = models.TextField(max_length=175)
    long_description = HTMLField()
    best_itinerary = models.BooleanField()
    rating =models.CharField(max_length=10, choices=RATING, default='')
    image = models.ImageField(upload_to='Itineraries')
    banner=models.ImageField(upload_to='Itineraries', default='')
    state = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('itinerary_detail',args=[self.country.country_slug,self.slug])

class Customized_Itinerary(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    mobile=models.CharField(max_length=12)
    name_itinerary = models.CharField(max_length=50,default='')
    continent=models.CharField(max_length=50,default='')
    country=models.CharField(max_length=50,default='')
    state=models.CharField(max_length=50,default='')
    budget=models.CharField(max_length=100)
    day=models.CharField(max_length=100)
    night=models.CharField(max_length=100)
    no_of_adults=models.IntegerField()
    no_of_childs=models.IntegerField()
    from_date=models.DateField()
    to_date=models.DateField()
    vacation=models.CharField(max_length=100)
    info=models.TextField(max_length=100)

    def __str__(self):
        return self.name

    def Send_Mail(self):
        return mark_safe('''<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#Modal%s">Send Mail</button>''' % self.id)
    title.short_description='Send Mail'
    title.allow_tags = True

    def Mail_modal(self):
        return mark_safe('''<div class="modal fade" id="Modal%s" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
            <form method="POST" action="/message/%s">
                <div class="mb-3">
                    <label for="formGroupExampleInput" class="form-label">Email</label>
                    <input type="text" class="form-control" value="%s" name="email" placeholder="Email Address" readonly>
                </div>
                <div class="mb-3">
                    <label for="text-area" class="form-label">Your message here</label>
                    <textarea rows="4" class="form-control" id="text-area" name="message" required></textarea>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Send</button>
            </div>
            </form>
            </div>
        </div>
        </div>''' % (self.id,self.id,self.email))
    title.short_description='Send Mail'
    title.allow_tags = True


    
class Cart(models.Model):
    cart_id=models.CharField(max_length=255,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Itinerarie,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    is_active=models.BooleanField(default=True)
    

    
    def __unicode__(self):
        return self.product   

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    #payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    countryphone_code = models.CharField(max_length=15,null=True,blank=True,default='')
    phone = models.CharField(max_length=15,null=True,blank=True)
    email = models.EmailField(max_length=50)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.order_number


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Itinerarie, on_delete=models.CASCADE)
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class Itinerariesimage(models.Model):
    post= models.ForeignKey(Itinerarie, on_delete=models.CASCADE)
    image= models.ImageField(upload_to="Itineraries")
    
    def _str_(self):
        return self.post.name

class Banner(models.Model):
    
    image=models.ImageField(upload_to='Itineraries')

class Newsletter(models.Model):
    email=models.EmailField(max_length=50)
    created_on = models.DateTimeField(auto_now=True)
