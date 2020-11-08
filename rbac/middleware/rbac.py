from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect,HttpResponse
import re

class RbacMiddleware(MiddlewareMixin):
    """
    权限控制的中间件
    """

    def process_request(self, request):
        """
        权限控制
        :param request:
        :return:
        """
        # 1. 获取当前请求URL
        current_url = request.path_info

        # 1.5 白名单处理
        for reg in settings.VALID_URL:
            if re.match(reg,current_url):
                return None

        # 2. 获取当前用户session中所有的权限
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return redirect('/login/')

        request.breadcrumb_list = [
            {'title': '首页', 'url': '/'},
        ]


        # 3. 进行权限校验
        flag = False
        for item in permission_dict.values():
            id = item['id']
            pid = item['pid']
            pname = item['pname']
            reg = "^%s$" % item.get('url')
            if re.match(reg, current_url):
                flag = True
                if pid:     # 访问的是添加客户
                    request.current_menu_id = pid
                    request.breadcrumb_list.extend([
                        {'title': permission_dict[pname]['title'], 'url': permission_dict[pname]['url']},
                        {'title': item['title'], 'url': item['url']},
                    ])
                else:
                    request.current_menu_id = id
                    request.breadcrumb_list.extend([
                        {'title': item['title'], 'url': item['url']},
                    ])
                break
        if not flag:
            return HttpResponse('无权访问')


