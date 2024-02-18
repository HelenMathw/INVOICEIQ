from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import RIVUE
from django.http import HttpResponseForbidden
from .forms import RIVUEForm
# Create your views here.
@login_required(login_url='login')

def HomePage(request):
    if request.method == "POST":
        form = RIVUEForm(request.POST, request.FILES)
        ProModel = request.POST['ProModel']
        ProName = request.POST['ProName']
        ProRev = request.POST['ProRev']
        ProEmail = request.POST['ProEmail']
        ProCom = request.POST['ProCom']
        data = RIVUE(ProModel=ProModel, ProName=ProName, ProRev=ProRev, ProEmail=ProEmail, ProCom= ProCom,user=request.user)
        data.save()
        if form.is_valid():
            form.instance.user = request.user  # Set the user from the request
            form.save()
            return redirect('show')
        return redirect('show')
    else:
        form=RIVUEForm()
    return render(request,'home.html')
    
def LandingPage(request):
    return render(request,'index.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        user = User.objects.create_user(uname, email, pass1)
        if pass1==pass2:
            return redirect('login')
        else:
            return HttpResponse("Your passwords do not match")
    return render(request,'signup.html')


def LoginPage(request):
    
    if request.method=='POST':
        username=request.POST.get('username')
        pass3=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass3)
        if user is not None:
            print("yes")
            login(request,user)
            print("yes")
            return redirect('home')
            
        else:
            return HttpResponse("Username or password is incorrect")
    return render(request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('index')

from django.http import JsonResponse



def success(request):
    return HttpResponse('successfully uploaded')