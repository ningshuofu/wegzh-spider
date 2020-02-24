from functools import wraps
import json

from django.http import QueryDict

from mysite.response import err_response


def validate_forms(form_class):
    """
    根据form模板类进行request表单验证
    :param form_class:
    :return:
    """
    def decorator(function):
        @wraps(function)
        def returned_wrapper(request):
            try:
                if request.method == "GET":
                    form = request.GET
                elif request.method == "POST":
                    if request.POST:
                        form = request.POST
                    else:
                        body = request.body.decode('utf-8')
                        form = json.loads(body)
                else:
                    form = QueryDict(request.body)
            except ValueError:
                return err_response('1002', '获取表单数据失败')

            form = form_class(form)
            if form.is_valid():
                data = form.cleaned_data
                return function(request, data)
            else:
                data = form.errors
                return err_response('1003', data)

        return returned_wrapper

    return decorator
