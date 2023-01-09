import csv
import os
# from waste import wasteSearch
from waste.settings import BASE_DIR
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from wasteSearch.models import WasteInfo
from wasteSearch import models
from django.conf import settings
from wasteSearch.utils.pagination import Pagination
from django.apps import apps
from wasteSearch.utils import search2
from wasteSearch.utils import getData
from django.db.models import Q
from django import forms
from wasteSearch.utils.createImage import check_code
from django.views.decorators.csrf import csrf_exempt
import json

select_labels =['废物类别', '别名', '产生工段', '表观形貌（稍微详细）', '物理形态', '形状', '颜色', '气味', '密度', '含水率', 'pH', '含油率', 'COD', '热值', '烧失率', '水分', '灰分', '挥发分', '固定碳', 'C', 'H', 'N', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', '', 'P', 'S', 'Cl', 'K', 'Ca', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'As', 'Pb', 'Ag', 'Bi', 'Cd', 'Sn', 'Sb', 'I', 'Hg', 'Ba', 'Al2O3', 'MgO', 'Cl', 'K2O', 'Na2O', 'Fe2O3', 'SiO2', 'MnO', 'CaO', 'S', 'SO3', 'As2O3', 'TiO2', 'Cr2O3', 'CuO', 'ZnO', 'PbO', 'F', 'V2O5', 'BaO', 'P2O5', 'SnO2', 'NiO', 'NaCl（%）', 'KCl', 'MgCl2', 'Mg(OH)2', 'Al(OH)3', 'AlCl3', 'MnCl2', 'NH4Cl（%）', 'TiCl4', 'FeCl2', 'FeCl3', 'CaCl2', 'CaF2', 'CaSO4', 'CaCO3', 'BaO', 'BaSO4', 'BaCO3', 'BaSiO3', 'BaS', 'NaNO3', '辉铜矿', '黄铜矿', '铜铁硫化相', '铁橄榄石', '磁铁矿', '钙铁辉石', '玻璃相', '石膏', '方解石', '石英', '砷铜矿', '皓矾', '六水锌矾', '氧化锑', '三氧化二砷', '五氧化二砷', '铅绿矾', '方铅矿', '铅黄', '铅', '密陀僧', '红锌矿', '闪锌矿', '锌', '纤锌矿', '冰晶石', '刚玉', 'β-氧化铝', '钾冰晶石', '铝', '锥冰晶石', '西蒙冰晶石', '氟铝钙锂石', '白砷石', '三水胆矾', '副雄黄', '砷华', '铅矾', '块黑铅矿', '四水锌矾', '硒汞矿', '尖晶石', '氮化铝', '方镁石', '铜靛矾', 'CuSO4•H2O', 'CdSO3•0.5H2O', '石盐', '氟氯铅矿', '铁白云石', '钙铝矾', '氯铅矿', 'T B(mg/kg)', 'T Na(mg/kg)', 'T Mg(mg/kg)', 'T Al(mg/kg)', 'T K(mg/kg)', 'T Ca(mg/kg)', 'T Fe', 'T Cu', 'T Pb', 'T Zn', 'T Sn', 'T Ni', 'T Co', 'T Sb', 'T Hg', 'T Cd', 'T Bi', 'T Cr（mg/kg）', 'T As', 'T Be', 'T Ba', 'T Pd', 'T Pt', 'T V', 'T Mn', 'T Ti', 'T Al3+ （mg/L）', 'T SO42- （g/L)', 'CN（mg/L)', 'F（mg/L)', '萘', '苊烯', '苊', '芴', '菲', '蒽', '荧蒽', '芘', '苯并（a）蒽', '屈', '苯并（b）荧蒽', '苯并 (k)荧蒽', '苯并（a）芘', '茚苯（1,2,3-cd）芘', ' 二苯并（a, n）蒽', '苯并（ghi）北（二萘嵌苯）', '乙酸乙酯', '乙酸丁酯', '乙酸异戊酯', '氨基甲酸乙酯', '邻甲酸甲酯', '邻甲基苯甲酸', '丁酸丁酯', 'N-氰基乙酰亚胺甲酯（乙酯）', '4-[3-甲基-3-(（甲亚基氨基)）苯基]丁酸乙酯', '氯甲酸甲酯', '邻苯二甲酸二甲酯', '邻甲基苯甲酸甲酯', '邻苯二甲酸二乙酯', '邻苯二甲酸二异丁酯', '邻苯二甲酸二正丁酯', '邻苯二甲酸二(2-甲氧基)乙酯', '邻苯二甲酸二(4-甲基-2-戊基)酯', '邻苯二甲酸二(2-乙氧基)乙酯', '邻苯二甲酸二戊酯', '邻苯二甲酸二己酯', '邻苯二甲酸丁基苄基酯', '邻苯二甲酸二(2-丁氧基)乙酯', '邻苯二甲酸二环己酯', '邻苯二甲酸二（2-乙基）己酯', '邻苯二甲酸二苯酯', '邻苯二甲酸二正辛酯', '邻苯二甲酸二壬酯', '苯', '甲苯', '乙苯', '二甲苯', '对二甲苯', '间二甲苯', '邻二甲苯', '异丙苯', '苯乙烯', '乙烯基甲苯', '环己烷', '二氯甲烷', '二氯乙烷', '苯酚', '邻甲酚', '2,4-二氯酚（mg/L）', '2,5-二氯苯酚（mg/L）', '甲醛%', '间苯氧基苯甲醛', '甲酸%', '苯氧乙酸（mg/L）', '氯乙酸', '羟基乙酸（mg/L)', '2甲4氯酸', '甲酸', '甘氨酸', '亚磷酸钠', '甲基草甘膦酸钠盐', '羟甲基磷酸钠盐', '2,4-二氯苯氧乙酸钠（mg/L)', '氯甲基吡啶', '吡啶', '2-氯-5-氯甲基吡啶', '三氯吡啶醇钠', '乙基氯化物', '氯乙酰氯', '邻苯二胺', '苯肼', '脲', '1-苯基氨基脲', '二甲胺', '2-氯烟酰胺', '精胺', '胺醚', '乙撑硫脲', '邻甲基苯基硫脲', '2-氯-N-(氯甲基)-N-(2,6-二乙基苯基)乙酰胺（MRM）', 'N-2,6-二乙基苯基甲亚胺（甲叉）', '丁草胺', '4-[3-乙基-2-(甲亚基氨基)苯基]丁酰氯', '2,5-二氯苯胺', '2,4-D（mg/L）', '草甘膦（mg/L)', '增甘膦mg/L', '双甘膦mg/L', '西玛津mg/L', '三唑磷mg/L', '烟嘧磺酰氯mg/L', '烟嘧磺胺mg/L', '烟嘧磺隆mg/kg', '毒死蜱', '多菌灵mg/L', '氟乐灵', '丁草胺mg/L', '咪鲜胺', '莠去津mg/L', '百草枯mg/L', '苯磺隆', '吡虫啉', '咪唑（烷）', '丙环唑', '代森锰mg/L', '敌百虫', '啶虫脒', '麦草畏', '杀虫单', '乙草胺', '溴丙烷', '四氯化碳', '丙溴磷', '对氯三氟甲苯', '功夫酰氯', '苄基三乙基氯化铵', '二氯菊酰氯', '4-甲基-2-肼基苯并骈噻唑', '苯唑醇', '二甲硫醚', '硫酸二甲酯', '甲醇', '乙醇', '辛硫磷', 'O,O-二乙基硫代磷酰氯', '2-氯烟酰胺', '二氯甲烷', '醋酸', '醋酸酐', '丙烯醛', '丙烯腈', '环戊二烯', 'L Ca(mg/L)', 'L Mg（mg/L)', 'L Fe (mg/L)', 'L Cu', 'L Pb', 'L Zn', 'L Ba (mg/L)', 'L Sn ', 'L Co', 'L Sb', 'L Hg', 'L Cd', 'L Bi', 'L Ni', 'L Cr （mg/L)', 'L Ag', 'L As', 'L Mn', 'L Se', 'L Br', 'L V']

def wasteAdd(request):

    context = {
        "select_label": select_labels,
    }

    if request.method == "GET":
       return render(request, "wasteAdd.html", context)



    wasteName = request.POST.get('morphology')
    print("wasteName: ", wasteName)
    Labels = request.POST.getlist('LabelName')
    print('LabelName: ', Labels)
    inputs = request.POST.getlist('q')
    print('inputs: ', inputs)
    waste_item = dict(zip(Labels, inputs))
    print('waste_item',waste_item)

    waste_file = request.FILES
    print('waste_file', waste_file)


    if not wasteName:
        return render(request, "wasteAdd.html", context)

    if waste_item == {'': ''}:
        if not waste_file:
            return render(request, "wasteAdd.html", context)
        # 处理文件上传逻辑

        # 获取文件对象
        wasteFile = request.FILES.get('wasteFile')
        file_path = os.path.join(settings.MEDIA_ROOT, wasteFile.name)
        f = open(file_path, mode='wb')
        for chunk in wasteFile.chunks():
            f.write(chunk)
        f.close()
        # 将文件保存到数据库中
        Img_newId = models.WasteImage.objects.count() + 1
        models.WasteImage.objects.create(
            dataId=Img_newId,
            wasteName=wasteName,
            img=file_path,
        )
        return render(request, "fileLoad.html", context)

    # 处理废物新增

    # 校验提交的数据是否重复
    print("(Not Labels and inputs null")
    if not (waste_item and wasteName):
        return render(request, "wasteAdd.html", context)

    waste_exist = models.WasteInfo.objects.filter(固废名称=wasteName).exists()
    if waste_exist:
        return render(request, "wasteAdd_repeat.html", context)

    # 其他校验

    # 将数据存入数据库
    newId = models.WasteInfo.objects.last().dataId + 1
    models.WasteInfo.objects.create(dataId=newId, 固废名称=wasteName)
    models.WasteInfo.objects.filter(dataId=newId).update(**waste_item)

    print("成功导入数据库")

    return render(request, "wasteAdd_success.html", context)


