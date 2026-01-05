from django.shortcuts import render,redirect
from django.contrib import messages
from Tracker.models import *
from django.db.models import Sum , Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def registration(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        
        user_obj = User.objects.filter(
            Q(email=email) | Q(username = username)
            )
        
        if user_obj.exists():
            messages.error(request,"UserName or Email ulready Exists")
            return redirect('registration')
        
        user_obj=User.objects.create(
                    first_name=first_name,
                    email=email,
                    username=username
                )
        user_obj.set_password(password)
        user_obj.save()
        messages.error(request,"Success : Account Created .")
        return redirect('login')

    return render(request,"registration.html")

def login_page(request):
    
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(
            username=username
            )
        
        if not user_obj.exists():
            messages.error(request,"Account notfound try registration")
        
        
        user_obj = authenticate(username=username, password = password)
        
        if not user_obj:
            messages.error(request,"Invalid Crediantial ..")
            
        login(request,user_obj)
        return redirect('index')
    
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url="/user_login/")      
def index(request):
    
    if request.method =="POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        
        if description is None:
            messages.info(request , "Description cannot be blank")
            return redirect('/')
        try:
            amount = float(amount)
        except Exception as e:
            messages.info(request, "Amount should be a number")
            return redirect('/')
            
    
        Transaction.objects.create(
            description=description,
            amount=amount,
            created_by = request.user
        )
        
    
        return redirect('/')
    
    balance = Transaction.objects.filter(created_by = request.user).aggregate(total_balance=Sum('amount'))['total_balance'] or 0
    income  = Transaction.objects.filter(created_by = request.user,amount__gte =0).aggregate(income = Sum('amount'))['income'] or 0
    expense = Transaction.objects.filter(created_by = request.user,amount__lte=0).aggregate(expense=Sum('amount'))['expense'] or 0
    
    context = {'transactions':Transaction.objects.filter(created_by = request.user),
               'balance':balance,
               'income':income,
               'expense':expense
               }
    return render(request, 'index.html' , context)

@login_required(login_url="/user_login/")    
def delete_transaction(request,uuid):
    Transaction.objects.get(uuid = uuid).delete()
    
    return redirect('/')