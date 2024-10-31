from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from cart.models import Cart,Payment,order_details
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
import razorpay

@login_required
def add_to_cart(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        c = Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            c.quantity+=1
            c.save()
            p.stock-=1
            p.save()

    except:
        c=Cart.objects.create(product=p,user=u,quantity=1)
        c.save()
        p.stock-=1
        p.save()

    return redirect('cart:cartview')

@login_required
def cart_view(request):
    u=request.user
    total=0
    c=Cart.objects.filter(user=u)
    for i in c:
        total+=i.quantity*i.product.price
    return render(request,'cart.html',{'cart':c,'total':total})


def cart_remove(request,i):
    p=Product.objects.get(id=i)
    u=request.user

    try:
        c=Cart.objects.get(user=u,product=p)
        if(c.quantity>1):
            c.quantity-=1
            c.save()
            p.stock+=1
            p.save()
        else:
            c.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return redirect('cart:cartview')

def cart_delete(request,i):
    p=Product.objects.get(id=i)
    u=request.user

    try:
        c=Cart.objects.get(user=u,product=p)
        c.delete()
        p.stock += c.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')

def order_form(request):
    if(request.method=="POST"):
        address=request.POST['a']
        phone=request.POST['p']
        pin=request.POST['pi']

        u=request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total+=i.quantity*i.product.price
        total=int(total*100)
        client=razorpay.Client(auth=('rzp_test_cQky6LUBsfvART','UOkwN4DKb9k2dZF8kDqedkA2')) #creates a client connection
        # using razorpay id and secret code

        response_payment=client.order.create(dict(amount=total,currency="INR"))  #creates an order with razorpay using razorpay client
        # print(response_payment)
        order_id=response_payment['id']  #Retrieves the order_id from response
        order_status=response_payment['status'] #retrive status from response
        if(order_status == "created"):  #if status is created then store order_id in payment and order_detail table
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=order_details.objects.create(product=i.product,user=u,no_of_items=i.quantity,address=address,phone_no=phone,pin=pin,order_id=order_id)
                o.save()
        else:
            pass

        response_payment['name']=u.username #additional information name

        return render(request,'payment.html',{'payment':response_payment})



    return render(request,'orderform.html')


@csrf_exempt
def payment_status(request,u):
    user = User.objects.get(username=u)
    if (not request.user.is_authenticated):  # if user is not authenticated
        login(request, user)  # allowing request user to login
    if (request.method == "POST"):
        response = request.POST
        print(response)
        print(u)

        param_dict = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature'],
        }

        client = razorpay.Client(auth=('rzp_test_cQky6LUBsfvART', 'UOkwN4DKb9k2dZF8kDqedkA2'))
        print(client)

        try:
            status=client.utility.verify_payment_signature(param_dict) #to check the authenticity of the razorpay signature
            print(status)
            # to retrieve a particular record in payment table whole order id matches the response order is
            p = Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id = response['razorpay_payment_id']  # adds the payment id after successfull payment
            p.paid = True  # changes paid status to true
            p.save()

            # user = User.objects.get(username=u)
            o = order_details.objects.filter(user=user, order_id=response['razorpay_order_id'])  # retrieve the particular record in order_details
            # matching with current user and response order_id
            for i in o:
                i.payment_status = "paid"
                i.save()

            # after successful payment deletes the item in cart for particular user
            c = Cart.objects.filter(user=user)
            c.delete()



        except:
            print("hello")



    return render(request, 'payment_status.html',{'status':status})

def order_view(request):
    u=request.user
    o=order_details.objects.filter(user=u)

    return render(request,'order_view.html',{'orders':o})
