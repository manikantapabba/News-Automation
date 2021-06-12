from django.shortcuts import render,redirect
from django.contrib import messages
from account.models import MyUser
from django.contrib.auth.models import auth
from news.models import Prefer

# Create your views here.

def home(request):

    if request.method == "POST":
        email = request.session.get('um')
        up = {}
        if(request.POST["msg_type"]!='none'):
            if(request.POST["msg_type"] =='remove'):
                up['msg_type'] = "none"
            else:
                up['msg_type'] = request.POST["msg_type"]
        if(request.POST["sports"]!='none'):
            if(request.POST["sports"] =='remove'):
                up['sports'] = "none" 
            else:
                up['sports'] = request.POST["sports"] 
        if(request.POST["entertainment"]!='none'):
            if(request.POST["entertainment"] =='remove'):
                up['entertainment'] = "none"
            else:
                up['entertainment'] = request.POST["entertainment"] 
        if(request.POST["business"]!='none'):
            if(request.POST["business"] =='remove'):
                up['business'] = "none" 
            else:
                up['business'] = request.POST["business"] 
        if(request.POST["technology"]!='none'):
            if(request.POST["technology"] =='remove'):
                up['technology'] = "none"
            else:
                up['technology'] = request.POST["technology"] 


        # up={
        # 'msg_type' : request.POST["msg_type"],
        # 'sports' : request.POST["sports"],
        # 'entertainment' : request.POST["entertainment"],
        # 'business' : request.POST["business"],
        # 'technology' : request.POST["technology"],  
        # }

        Prefer.objects.filter(email = email).update(**up)

        details = Prefer.objects.get(email = email)
        
        return render(request,'index.html',{'details':details})
    
    else:
        if request.session.has_key("um"):
            email = request.session.get('um')
            details = Prefer.objects.get(email = email)
            return render(request,'index.html',{'details':details})
        else:
            return render(request,'index.html')

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['um'] = email
            return redirect("index_page")
        else:
            messages.info(request,"invalid credentials")
            return redirect("login_page")

    else:
        return render(request,'login.html')

def Signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        phone = request.POST['number']
        password = request.POST['password']
        password_check = request.POST['re-password']
        if password == password_check:
            if MyUser.objects.filter(email=email).exists():
                messages.info(request,"Already Registered with this email")
                return redirect("signup_page")
            else:
                user = MyUser.objects.create_user(email=email,phone=phone,password=password)
                user.save()
                addprefer = Prefer.objects.create(email=email)
                addprefer.save()
                return redirect("index_page")
        else:
            messages.info(request,"Please re-enter correct password")
            return redirect("signup_page")    
    else:
            return render(request,'signup.html')


def Logout(request):
    auth.logout(request)
    return redirect("index_page")