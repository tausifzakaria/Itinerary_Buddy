from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import *
from django.contrib.auth.models import Group

from import_export.admin import ExportActionMixin

# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    list_display = ["image"]


admin.site.register(Banner, BannerAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ["country_name"]
    prepopulated_fields = {"country_slug": ("country_name",)}


admin.site.register(Country, CountryAdmin)


class ContinentAdmin(admin.ModelAdmin):
    list_display = ["continent_name"]
    prepopulated_fields = {"continent_slug": ("continent_name",)}


admin.site.register(Continent, ContinentAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = ["city_name"]
    prepopulated_fields = {"slug": ("city_name",)}


admin.site.register(City, CityAdmin)


class Customized_ItineraryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "mobile",
        "name_itinerary",
        "budget",
        "day",
        "night",
    )

    change_form_template = "includes/send_email.html"

    def response_change(self, request, obj):
        if "_make-unique" in request.POST:
            matching_names_except_this = (
                self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
            )
            matching_names_except_this.delete()
            obj.is_unique = True
            obj.save()
            self.message_user(request, "check")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(Customized_Itinerary, Customized_ItineraryAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ["product", "is_active"]


admin.site.register(CartItem, CartItemAdmin)

admin.site.unregister(Group)


admin.site.register(Cart)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = (
        "payment",
        "user",
        "product",
    )
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "phone",
        "email",
        "tax",
        "status",
        "is_ordered",
        "created_at",
    ]
    list_filter = ["status", "is_ordered"]
    search_fields = ["order_number", "phone", "email"]
    list_per_page = 20
    inlines = [OrderProductInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "payment_id", "amount_paid", "status"]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderProduct)


class ItinerariesimageAdmin(admin.StackedInline):
    model = Itinerariesimage


class ItinerariesAdmin(admin.ModelAdmin):
    # list_display=['name','small_description']
    inlines = [
        ItinerariesimageAdmin,
    ]
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        model = Itinerariesimage


admin.site.register(Itinerarie, ItinerariesAdmin)


class ItinerariesimageAdmin(admin.ModelAdmin):
    list_display = ["post", "image"]


# admin.site.register(Itinerariesimage)


class NewsletterAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["email", "created_on"]


admin.site.register(Newsletter, NewsletterAdmin)

admin.site.register(OrderProduct)
