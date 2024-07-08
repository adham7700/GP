from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField




class Profile (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image= models.ImageField(default='default.jpg' ,upload_to= 'profile_pics') 
    phone_number = models.CharField(max_length=11,blank=True)
    # phone_number = PhoneNumberField(blank=True)
    # phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='egp'))

    parentName =models.CharField(max_length=20,default='NULL')
    note = models.TextField(default='NULL')
    parentName =models.CharField(max_length=20,default='NULL')

    def __str__(self):
        return f'{self.user.username} Profile'    
    
    
    