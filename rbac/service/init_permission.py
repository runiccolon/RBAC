from django.conf import settings


def init_permission(request, user):
    """
    权限和菜单信息初始化,使用时需要在登陆成功后调用该方法
    :param request:
    :param user:
    :return:
    """
    # 3. 获取用户信息和权限信息写入session
    permission_queryset = user.roles.filter(permissions__url__isnull=False).values('permissions__url',
                                                                                   'permissions__title',
                                                                                   'permissions__menu_id',
                                                                                   'permissions__menu__title',
                                                                                   'permissions__menu__icon').distinct()
    menu_dict = {}  # 菜单+能成为菜单的权限
    permission_list = []    # 所有权限，用作权限校验
    for row in permission_queryset:
        permission_list.append({'permissions__url': row['permissions__url']})
        menu_id = row.get('permissions__menu_id')
        if not menu_id:
            continue
        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                'title': row['permissions__menu__title'],
                'icon': row['permissions__menu__icon'],
                'children': [
                    {'title': row['permissions__title'], 'url': row['permissions__url']}
                ]
            }
        else:
            menu_dict[menu_id]['children'].append({'title': row['permissions__title'], 'url': row['permissions__url']})

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict
