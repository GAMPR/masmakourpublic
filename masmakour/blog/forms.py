from django import forms
from .models import Comment, Contact
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User 
#from django.conf import settings
from django.contrib.auth import get_user_model 
from captcha.fields import ReCaptchaField


#create your forms here 
#necessary for custom user model 
User = get_user_model() 

#class form
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__' 


#new user form 
class NewUserForm(UserCreationForm):

    email = forms.EmailField(required = True)
    captcha = ReCaptchaField() 

    class Meta:
        model = User
        #model = settings.AUTH_USER_MODEL 
        fields = ("username", "email", "password1", "password2", "captcha") 

    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit = False) 
        user.email = self.cleaned_data['email'] 
        if commit:
            user.save()
        return user

#comment form 
class CommentForm(forms.ModelForm):
   
    class Meta:
        model = Comment
        fields = ('body',)

    def save(self, commit = True):
        comment = super(CommentForm, self,).save(commit = False) 
        if commit:
            comment.save() 
        return comment

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ""
    
    
#about me form 
class AboutForm(forms.ModelForm):
 
    class Meta:
        model = User
        fields = ('about',)

#email form 
class EmailForm(forms.ModelForm):
 
    class Meta:
        model = User
        fields = ('email',)

    

