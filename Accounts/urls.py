from django.urls import path
from .import views


urlpatterns = [

       path('register/',views.register,name="register"),
       path('login/',views.login,name="login"),
       path('activate/<uidb64>/<token>/',views.activate,name="activate"),
       path('logoutUser/',views.logoutUser,name="logoutUser"),
       path('forgotpassword/',views.forgotpassword,name="forgotpassword"),
       path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name="resetpassword_validate"),
       path("resetpassword/",views.resetpassword,name="resetpassword"),
       path('change_password/',views.change_password,name='change_password'),
   
  

]