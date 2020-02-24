from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from mysite.decorator import validate_forms
from mysite.forms import Upload, Get
from mysite.model import User
from mysite.response import err_response, corr_response


@transaction.atomic()
@validate_forms(Upload)
def upload(request, data):
    """
    # 客户端上传客户端号和分数
    :param request:
    :param data:
    :return:
    """
    no = data['no']
    score = data['score']
    try:
        user = User.objects.select_for_update().get(no=no)
        user.score = score
    except ObjectDoesNotExist:
        user = User(no=no, score=score)
    try:
        user.save()
    except Exception:
        return err_response('1000', '数据库保存数据失败，请重试')
    return corr_response()


@validate_forms(Get)
def get(request, data):
    """
    # 客户端查询排行榜
    :param request:
    :param data:
    :return:
    """
    no = data['no']
    start = data['start']
    end = data['end']
    try:
        rank_list = User.objects.all().order_by('score')[start:end]
    except Exception:
        return err_response('1001', '数据库获取数据出错')
    try:
        rank = User.objects.get(no=no)
    except ObjectDoesNotExist:
        return err_response('1004', '数据库无此用户数据')
    return_list = [(i.no, i.score) for i in rank_list]
    return_list.append((rank.no, rank.score))

    return corr_response(return_list)
