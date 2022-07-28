from django import forms
from django.core.validators import ValidationError
from orders.models import Order


class CartAddFormForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if int(quantity) <= 0:
            raise ValidationError('تعداد باید بیشتر از 1 باشد')
        return quantity


class CouponCodeForm(forms.Form):
    code = forms.CharField(max_length=100, required=True)


class OrderCheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('recipient_name', 'recipient_phone_number', 'recipient_address')

    def clean_recipient_name(self):
        recipient_name = self.cleaned_data['recipient_name']
        if len(recipient_name) < 5:
            raise ValidationError('نام گیرنده را کامل وارد کنید')
        return recipient_name

    def clean_recipient_phone_number(self):
        recipient_phone_number = self.cleaned_data['recipient_phone_number']
        if len(recipient_phone_number) != 11:
            raise ValidationError('شماره تلفن وارد شده معتبر نمی‌باشد')
        return recipient_phone_number

    def clean_recipient_address(self):
        recipient_address = self.cleaned_data['recipient_address']
        if len(recipient_address) < 10:
            raise ValidationError('آدرس گیرنده را کامل وارد کنید')
        return recipient_address
