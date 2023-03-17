from itertools import product
from urllib import request
from django.shortcuts import render,redirect

from seller.models import *

# Create your views here.

def seller_login(request):
    if request.method=='POST':
        try:
            sellerobj = Seller.objects.get(email=request.POST['email'])
            if request.POST['password'] == sellerobj.password:
                request.session['email']=request.POST['email']
                request.session['name']=sellerobj.name
                return render(request,'seller-index.html')
            else:
                return render(request,'seller-login.html',{'msg':'wrong password'})
        except:
            return render(request,'seller-login.html',{'msg':'Email Not Found'})
    return render(request,'seller-login.html')

def seller_index(request):
    return render(request,'seller-index.html')

def seller_addproduct(request):
    sellerobj=Seller.objects.get(email=request.session['email'])
    if request.method=='POST':
        
           
        Product.objects.create(
        name=request.POST["pname"],
        des=request.POST["desc"],
        price=request.POST["price"],
        quantity=request.POST["quantity"],
        discount=request.POST["discount"],
        seller=sellerobj,
        pic=request.FILES['img']
        )
        
    return render(request,'seller-addproduct.html')

def manageproduct(request):
    sellerobj=Seller.objects.get(email=request.session['email'])
    pobj= Product.objects.filter(seller=sellerobj)
    return render(request,'seller-manageproduct.html',{'productlist':pobj})

def edit(request,pid):
    productobj=Product.objects.get(id=pid)  # to recieve product from pid
    if request.method=='POST':
        productobj.name=request.POST["pname"]
        productobj.des=request.POST["desc"]
        productobj.price=request.POST["price"]
        productobj.quantity=request.POST["quantity"]
        productobj.discount=request.POST["discount"]
        productobj.save()
        return redirect('manageproduct')
    return render(request,'seller-editproduct.html',{'productitem':productobj})

def delete(request,pid):
    productobj=Product.objects.get(id=pid)  # to recieve product from pid
    if request.method=='POST':
        productobj.delete()
        return redirect('manageproduct')
    return render(request,'seller-deleteproduct.html',{'productitem':productobj})