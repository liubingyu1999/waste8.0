from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

# 定义中间件

class AuthMiddleware(MiddlewareMixin):
    """" 中间件 """
    def process_request(self, request):
        # 若方法没有返回值 返回None 继续向后走
        # 若有返回值 HttpResponse
        #print("中间件，进来了")
        if request.path_info in ["/login/", "/image/code/"]:
            return

        """读取当前访问用户的session信息，若能读到 说明已登录"""
        info_dict = request.session.get("info")
        #print("info_dict",info_dict)
        if info_dict:
            return

        """没有登录过,回到登录界面"""

        return redirect('/login/')

    def process_response(self, request, response):
        #print("中间件，出去了")
        return response




