from django import forms


# 客户端上传客户端号和分数
class Upload(forms.Form):
    # 客户端号
    no = forms.IntegerField()
    # 分数
    score = forms.IntegerField(min_value=1, max_value=10000000)


# 客户端查询排行榜
class Get(forms.Form):
    # 客户端号
    no = forms.IntegerField()
    # 查询初始排名
    start = forms.IntegerField()
    # 查询最末排名
    end = forms.IntegerField()
