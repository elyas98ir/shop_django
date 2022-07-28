from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json
from .models import Payment
from products.models import Product
from .cart import Cart


MERCHANT = '1344b5d4-0048-11e8-94db-005056a205be'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://zarinpal.com/pg/StartPay/{authority}"
CallbackURL = 'http://127.0.0.1:8000/orders/pay/verify/'


def send(request, order):
    user = request.user
    if order.coupon_code and order.coupon_discount:
        amount = order.get_total_cost(without_discount=False)
    else:
        amount = order.get_total_cost(without_discount=True)
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount * 10,
        "callback_url": CallbackURL,
        "description": f'تراکنش کاربر {user.id} برای سفارش {order.id}',
        "metadata": {"mobile": user.phone_number, "email": user.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)

    if req.status_code == 500:
        return HttpResponse('خطا در اتصال به درگاه پرداخت')

    if len(req.json()['errors']) == 0:
        authority = req.json()['data']['authority']
        Payment.objects.create(user=user, order=order, amount=amount, authority=authority)
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    payment = Payment.objects.get(authority=t_authority)
    order = payment.order
    user = payment.user
    if t_status == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": payment.amount * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)

        if req.status_code == 500:
            return HttpResponse('خطا در اتصال به درگاه پرداخت')

        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                payment.status = True
                payment.tracking_code = str(req.json()['data']['ref_id'])
                payment.save()
                order.paid = True
                order.save()

                for item in order.items.all():
                    product = item.product
                    product.stock_quantity = product.stock_quantity - item.quantity
                    product.save()

                cart = Cart(request)
                cart.clear()

                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code},\nError Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')
