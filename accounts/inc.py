from .models import OTPCode, User
import random
from django.utils import timezone
from datetime import timedelta


# for otp get request
def get_user_otp(phone_number):
    valid_time = timezone.now() - timedelta(minutes=2)
    try:
        return OTPCode.objects.get(phone_number=phone_number, created__gt=valid_time)
    except OTPCode.DoesNotExist:
        return None


def create_code(phone_number):
    otp = get_user_otp(phone_number)
    if otp is None:
        code = random.randint(10000, 99999)
        otp = OTPCode.objects.create(phone_number=phone_number, code=code)
    return otp


# for otp post request
def check_otp(phone_number, code):
    valid_time = timezone.now() - timedelta(minutes=2)
    try:
        return OTPCode.objects.get(phone_number=phone_number, code=code, created__gt=valid_time)
    except OTPCode.DoesNotExist:
        return None


def get_or_create_user(phone_number):
    try:
        return User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return User.objects.create(phone_number=phone_number)


def delete_codes(phone_number):
    OTPCode.objects.filter(phone_number=phone_number).delete()


def verify_code(phone_number, code):
    otp = check_otp(phone_number, code)
    if otp:
        get_or_create_user(phone_number)
        delete_codes(phone_number)
        return True
    return False
