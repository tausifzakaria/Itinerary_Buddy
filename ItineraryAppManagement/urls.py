from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('about',views.about,name="about"),
    path('added_cart/<str:product_id>/',views.added_cart,name="added_cart"),
    path('add_cart/<str:product_id>/',views.add_cart,name="add_cart"),

    path('customized_itinerary',views.customized_itinerary,name="customized_itinerary"),
    path('checkout/',views.checkout,name="checkout"),
    path('cart/',views.cart,name="cart"),
    path('country/<slug:country_slug>',views.itinerary,name="country_detail"),

    path('dashboard/',views.dashboard,name="dashboard"),

    path('itinerary',views.itinerary,name="itinerary"),
    path('itinerary/<slug:country_slug>/<slug:itineraries_slug>/',views.itinerary_details,name="itinerary_detail"),

    path('my_profile',views.my_profile,name="my_profile"),
    path('message',views.send_message,name="send_message"),

    path('newsletter/',views.newsletter,name="newsletter"),

    path('profile/<str:id>',views.profile,name="profile"),
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('payment_done/<str:id>',views.payment_done,name='payment_suc'),

    path("remove_cart_item/<int:product_id>/<int:cart_item_id>/",views.remove_cart_item,name='remove_cart_item'),
    path('render_pdf/<str:id>/',views.render_pdf_view,name='render_pdf'),
    path('render_pdf_itinerary/<str:id>/',views.render_pdf_view_itinerary,name='render_pdf_itinerary'),
    path('razorpay/<str:id>/',views.razorpay,name='razorpay'),

    path('state/<slug:country_slug>/<slug:city_slug>',views.itinerary,name="city_detail"),
    path('search/',views.search,name="search"),
]


