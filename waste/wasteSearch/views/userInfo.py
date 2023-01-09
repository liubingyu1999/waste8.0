from django.shortcuts import render, redirect

from wasteSearch import models
from wasteSearch.utils.pagination import Pagination
from wasteSearch.utils.bootstrap import BootStrapModelForm
from django.core.exceptions import ValidationError
from wasteSearch.utils.encrypt import md5
def userList(request):


    """ 搜索 """
    data_dict = {}
    search_data = request.GET.get('q',"")
    if search_data:
        data_dict["username__contains"] = search_data

    """根据搜索条件 获取用户列表"""
    queryset = models.Admin.objects.filter(**data_dict)

    """分页内容"""
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'userList.html', context)



from django import forms
class UserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.Admin
        fields = ['username','password']
        widgets = {
            "password":forms.PasswordInput(render_value=True)
    }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm
def userAdd(request):
    """添加用户"""
    title = "添加用户"
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'userAdd.html',{'form': form,"title":title})

    """获取用户类型和用户状态"""

    type = request.POST.get("inputType")
    state = request.POST.get("inputState")

    form = UserModelForm(data=request.POST)

    if form.is_valid():
        #print(form.cleaned_data)
        #print("form",form)
        """判断用户名是否已存在"""
        input_name = form.cleaned_data.get("username")
        user_exist = models.Admin.objects.filter(username=input_name).exists()

        if user_exist:
            form.add_error("username", "用户名已存在")
            return render(request, 'userAdd.html', {'form': form})

        """将验证通过的数据存储到数据库中"""
        models.Admin.objects.create(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password"),
            usertype=type,
            userstate=state,
        )
        #form.save()
        return redirect('/user/list/')

    return render(request,'userAdd.html', {'form': form})


def userEdit(request, nid):
    """ 修改用户信息 """
    #是否能获得当前对象
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/user/list/')

    title = "修改用户信息"
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        print(row_object)
        return render(request, "userAdd.html", {"title": title,'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    type = request.POST.get("inputType")
    state = request.POST.get("inputState")
    if form.is_valid():
        """ 判断用户是否修改用户名 """
        oldName = models.Admin.objects.filter(id=nid).first().username
        input_name = form.cleaned_data.get("username")
        if oldName != input_name:
            user_exist = models.Admin.objects.filter(username=input_name).exists()
            if user_exist:
                form.add_error("username", "用户名已存在")
                return render(request, 'userAdd.html', {'form': form})

        """将验证通过的数据存储到数据库中"""
        models.Admin.objects.filter(id=nid).update(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password"),
            usertype=type,
            userstate=state,
        )

        # form.save()
        return redirect('/user/list/')

    return render(request,"userAdd.html",{"title": title})

def userDelete(request,nid):
    """删除用户"""
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/user/list/')


class UserResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.Admin
        fields =['password','confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 数据库校验输入的密码是否更新
        exist = models.Admin.objects.filter(id=self.instance.pk, password=pwd).exists()
        if exist:
            raise ValidationError("密码不能与之前密码一致")
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm

def userReset(request,nid):
    """重置密码 """
#是否能获得当前对象
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/user/list/')


    title = "重置密码 - {}".format(row_object.username)

    if request.method == "GET":
        form = UserResetModelForm()
        return render(request, "userResetPassword.html", {"form": form, "title": title})

    form = UserResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        """将验证通过的数据存储到数据库中"""
        form.save()
        return redirect('/user/list/')

    return render(request, "userResetPassword.html", {"form": form, "title": title})
