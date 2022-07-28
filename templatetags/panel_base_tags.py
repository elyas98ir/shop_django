from django import template
# from extensions.utils import jalali_converter
# from django.utils import timezone


register = template.Library()


@register.inclusion_tag('panel/partials/nav_item.html')
def nav_item(request, url_name, text):
    return {
        'request': request,
        'url_name': url_name,
        'go_to': f'panel:{url_name}',
        'text': text,
    }


@register.inclusion_tag('panel/partials/nav_menu.html')
def nav_menu(request, url_names, href, text, icon):
    return {
        'request': request,
        'url_names': url_names.split(','),
        'href': href,
        'text': text,
        'icon': icon,
    }


@register.inclusion_tag('panel/partials/nav_active.html')
def nav_active(request, url_names):
    return {
        'request': request,
        'url_names': url_names.split(','),
    }


# @register.inclusion_tag('panel/partials/jalali_date.html')
# def jalali_date(date):
#     return {
#         'date': jalali_converter(timezone.make_aware(date)),
#     }
