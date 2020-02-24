from django.http import JsonResponse

# logger = logging.getLogger('django.request')


def corr_response(data=None):
    """正确时的返回
    :param data: 字典
    """
    # str_data = str(data) if data is not None else ''
    # logger.info(len(str_data))

    if data is None:
        params = {
            "status": True,
        }
    else:
        params = {
            "status": True,
            "data": data
        }
    return JsonResponse(params)


def err_response(err_code, description):
    """发生错误时的返回
    :param err_code: 错误码字符串
    :param description: 错误描述
    """
    # logger.info('error response')

    params = {
        "status": False,
        "err_code": err_code,
        "description": description
    }
    return JsonResponse(params)
