from . import jalali
from django.utils import timezone


def jalali_converter(time, type='all'):

    jmonths = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

    time = timezone.localtime(time)
    time_to_str = f'{time.year},{time.month},{time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = ''
    hour = time.hour
    minute = time.minute

    if time.hour < 10:
        hour = f'0{time.hour}'

    if time.minute < 10:
        minute = f'0{time.minute}'

    if(type == 'all'):
        output = '{} {} {} ، ساعت {}:{}'.format(
            time_to_list[2],
            time_to_list[1],
            time_to_list[0],
            hour,
            minute
        )
    elif(type == 'short'):
        output = '{} {} {}'.format(
            time_to_list[2],
            time_to_list[1],
            time_to_list[0],
            hour,
            minute
        )
    elif(type == 'day'):
        output = time_to_list[2]
    elif(type == 'month'):
        output = time_to_list[1]
    elif(type == 'year'):
        output = time_to_list[0]
    else:
        output = time

    return output
