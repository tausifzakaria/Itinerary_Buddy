from django import forms
from .models import Account
from django.contrib.auth.password_validation import validate_password
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
      'class':'form-control',
      'placeholder':'Enter Password',

    }))
    
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
      'class':'form-control',
      'placeholder':'Confirm Password',

    }))
    username=forms.CharField(widget=forms.TextInput(attrs={
      'class':'form-control',
      'placeholder':'Enter Username',

    }))
    email=forms.EmailField(widget=forms.EmailInput(attrs={
      'class':'form-control',
      'placeholder':'Enter Email',

    }))
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    
    class Meta:
        model=Account
        fields=[ 'email', 'password']



    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
          # print(range(password))
          raise forms.ValidationError(
            "password does not match"   ) 
        
        # elif range(password) < 8:
        #   raise forms.ValidationError(
        #     "Password too short"   ) 

class UserprofileForm(forms.ModelForm):
  class Meta:
    model =Account
    fields = ("username","email","mobile","nationality","country","profile_pic")  
    
  def save(self, commit: True):
    profileupdate = self.instance
    profileupdate.username = self.cleaned_data['username']
    profileupdate.email = self.cleaned_data['email']
    profileupdate.mobile = self.cleaned_data['mobile']
    profileupdate.nationality = self.cleaned_data['nationality']
    profileupdate.country = self.cleaned_data['country']
    
    if self.cleaned_data['profile_pic']:
      profileupdate.profile_pic = self.cleaned_data['profile_pic']
    
    if commit:
      profileupdate.save()
    return profileupdate