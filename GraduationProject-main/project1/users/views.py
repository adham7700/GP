from django.shortcuts import render ,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm ,UserUpdateForm, ProfileUpdateForm
# Create your views here.
from django .contrib.auth.decorators import login_required


def register(request):
    if request.method =='POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user =form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect ('login')
    else:
        form=UserRegisterForm()
    
    return render(request, 'users/register.html', {'form':form})
    
    
    
@login_required
def profile(request):
    if request.method =='POST':
        u_form =UserUpdateForm(request.POST ,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
    
    else:
        u_form =UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context ={
    
    "u_form" : u_form,  
    "p_form":p_form 
    }
    
    
    return render(request,'users/profile.html',context)
