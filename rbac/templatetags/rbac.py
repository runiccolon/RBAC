from django.template import Library
from django.conf import settings
import re
from collections import OrderedDict
register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """
    生成菜单
    :param request:
    :return:
    """

    menu_dict = request.session.get(settings.MENU_SESSION_KEY)

    ordered_dict = OrderedDict()
    for key in sorted(menu_dict):
        ordered_dict[key] = menu_dict[key]
        menu_dict[key]['class'] = 'hide'

        for node in menu_dict[key]['children']:
            if request.current_menu_id == node['id']:
                node['class'] = 'active'
                menu_dict[key]['class'] = ''

    return {'menu_dict':ordered_dict}

@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'breadcrumb_list':request.breadcrumb_list}

@register.filter
def has_permission(request,name):
    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
    if name in permission_dict:
        return True