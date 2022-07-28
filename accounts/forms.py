from django import forms
from django.core.exceptions import ValidationError


class UserOTPSendForm(forms.Form):
    phone_number = forms.CharField(max_length=11)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) == 11 and phone_number.startswith('09'):
            return phone_number
        raise ValidationError('شماره تلفن وارد شده معتبر نمیباشد')


class UserOTPVerifyForm(forms.Form):
    code = forms.CharField(max_length=5)

    def clean_code(self):
        code = self.cleaned_data['code']
        if len(code) == 5:
            return code
        raise ValidationError('کد تایید باید 5 رقمی باشد')
