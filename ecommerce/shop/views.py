from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def allcategories(request):
    c = Category.objects.all()
    return render(request, 'category.html', {'cat': c})

def allproducts(request,p):
    c=Category.objects.get(id=p)
    p=Product.objects.filter(category=c)

    return render(request,'product.html',{'cat':c,'product':p})

def productdetails(request,p):
    p=Product.objects.get(id=p)
    return render(request,'detail.html',{'product':p})

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        cp=request.POST['cp']
        f=request.POST['f']
        l=request.POST['l']
        e=request.POST['e']

        if(p==cp):
            u=User.objects.create_user(username=u,password=p,first_name=f,last_name=l,email=e)
            u.save()
        else:
            return HttpResponse("password are not matching")
        return redirect('shop:login')
    return render(request,'register.html')

def user_login(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u, password=p)

        if user:
            login(request, user)
            return redirect('shop:category')
        else:
            # This is where we send an invalid credential error message
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('shop:login')  # Reload the login page

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('shop:login')

def addcategory(request):
    if request.method=='POST':
        name= request.POST['n']
        desc=request.POST['d']
        image=request.FILES['i']

        k=Category.objects.create(name=name,desc=desc,image=image)
        k.save()
        return redirect('shop:category')
    return render(request,'addcategory.html')

def addproduct(request):
    if request.method=='POST':
        name= request.POST['n']
        desc=request.POST['d']
        image=request.FILES.get('i')
        price=request.POST['p']
        stock=request.POST['s']
        category = request.POST['c']  #read category name from the field
        m=Category.objects.get(name=category)  #category object/record matching with category name c
        k=Product.objects.create(name=name,desc=desc,image=image,price=price,stock=stock,category=m)  #assigns each value to product field
        k.save()

        return redirect('shop:category')
    return render(request, 'addproduct.html')

def add_stock(request,p):
    pro=Product.objects.get(id=p)
    if(request.method=="POST"):
        pro.stock=request.POST['n']
        pro.save()
        return redirect('shop:category')
    return render(request,'addstock.html',{'product':pro})





