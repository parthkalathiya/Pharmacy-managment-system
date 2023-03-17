from django.shortcuts import render,redirect
from django.http import JsonResponse
from myapp.models import *
from seller.models import *
from django.conf import settings
# import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


def index(request):
    return render(request,'index.html')




def login(request):
    if request.method=='POST':
        try:
            userobj = User.objects.get(email=request.POST['email'])
            if request.POST['password'] == userobj.password:
                request.session['email']=request.POST['email']
                request.session['name']=userobj.name
                return redirect('index')
        except:
            return render(request,'login.html',{'msg':'Email Not Registered'})

    return render(request,'login.html')


 
def register(request):
    if request.method=='POST':
        if request.POST['pass']==request.POST['cnfpass']:
            User.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                password=request.POST['pass']
            )
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'msg':'Passwords did not match.!'})
    return render(request,'register.html')

    
def contact(request):
    return render(request,'contact.html')

def products(request):
    plist = Product.objects.all()
    for item in plist:
        item.discountedprice=item.price-(item.price*item.discount/100)

    return render(request,'products.html',{'productlist':plist})    

def single(request,pid):
    pobj = Product.objects.get(id=pid)
    pobj.discountedprice=pobj.price-(pobj.price*pobj.discount/100)
    return render(request,'single.html',{'pobj':pobj})

def addtocart(request):
    pid=request.GET['pid']
    userobj = User.objects.get(email=request.session['email'])
    pobj = Product.objects.get(id=pid)

    Cart.objects.create(
        product=pobj,
        user=userobj,
        quantity=1
    )
    return JsonResponse({'msg':'Product Added'})

def cart(request):
    userobj = User.objects.get(email=request.session['email'])
    cartitems=Cart.objects.filter(user=userobj)

    carttotal=0
    for item in cartitems:
        dp=item.product.price-(item.product.price*item.product.discount/100)
        item.product.discountedprice=dp*item.quantity
        carttotal+=item.product.discountedprice

    return render(request,'cart.html',{'cartitems':cartitems,'carttotal':carttotal})

        # razorpay_client = razorpay.Client(
        #     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))    

# def pay(request):
#     userobj = User.objects.get(email=request.session['email'])
#     orderobj = Order.objects.create(
#         user=userobj,
#         order_status='Confirmed'
#     )

#     cartdata=Cart.objects.filter(user=userobj)
#     s = 0
#     for i in cartdata:
#         s +=  int(i.product.price)
    
#     for item in cartdata:
#         OrderDetails.objects.create(
#             product=item.product,
#             quantity=item.quantity,
#             order=orderobj
#         )

#     currency = 'INR'
#     amount = s*100  # Rs. 200
 
#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = f'paymenthandler/{userobj.id}'    # callback url with order id
 
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url

#     return render(request,'pay.html',context=context)

# @csrf_exempt
# def paymenthandler(request,oid):
 
#     # only accept POST request.
#     if request.method == "POST":
#         try:
#             order = Order.objects.get(id = oid)
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
 
#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             # if result is None:
#             amount = (order.amount)*100  # Rs. 200
#             try:

#                 # capture the payemt
#                 razorpay_client.payment.capture(payment_id, amount)
#                 order.pay_id = payment_id   # payment ID update
#                 order.verify = True
#                 order.save()
#                 # render success page on successful caputre of payment
#                 return render(request, 'success.html')
#             except:

#                 # if there is an error while capturing payment.
#                 return render(request, 'fail.html')
#             # else:
 
#             #     # if signature verification fails.
#             #     return render(request, 'paymentfail.html')
#         except:
 
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()