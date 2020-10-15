from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    #every time form is submitted this function will be called
    #overriding default clean funtion
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        #if both firld are filled
        if username and password:
            user = authenticate(username=username,password=password)
            
            # if no such user found
            if not user:
                raise forms.ValidationError("User does not exists")
            
            #if password is wrong
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")

            if not user.is_active:
                raise forms.ValidationError("User not active")
        
        #calling main clean function
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(label="Email-id")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password', 'confirm_password']

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if email_qs.exists():
            raise forms.ValidationError("This email is already registered") 
        if password != confirm_password:
            raise forms.ValidationError("Password does not match")
        return super(UserRegisterForm, self).clean(*args, **kwargs)

    




    