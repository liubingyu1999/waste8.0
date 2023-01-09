import os

from django.shortcuts import render, redirect

from waste import settings
from wasteSearch import models
from wasteSearch.utils.pagination import Pagination
from wasteSearch.utils.bootstrap import BootStrapModelForm
from wasteSearch.utils.getData import verbosename2name
from django.core.exceptions import ValidationError
from wasteSearch.utils.encrypt import md5


labels = ['行业分类', '固废名称', '别名', '产生工段', '表观形貌稍微详细', '表观形貌关键词', '物理形态', '形状', '颜色', '气味', '密度', '含水率', 'pH', '含油率', 'COD', '热值', '烧失率', '水分', '灰分', '挥发分', '固定碳', 'C', 'H', 'N', 'O', 'F', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'K', 'Ca', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'As', 'Pb', 'Ag', 'Bi', 'Cd', 'Sn', 'Sb', 'I', 'Hg', 'Ba', 'Al2O3', 'MgO', 'P_Cl', 'K2O', 'Na2O', 'Fe2O3', 'SiO2', 'MnO', 'CaO', 'P_S', 'SO3', 'As2O3', 'TiO2', 'Cr2O3', 'CuO', 'ZnO', 'PbO', 'P_F', 'V2O5', 'BaO', 'P2O5', 'SnO2', 'NiO', 'NaCl', 'KCl', 'MgCl2', 'MgOH2', 'AlCl3', 'MnCl2', 'NH4Cl', 'TiCl4', 'FeCl2', 'FeCl3', 'CaCl2', 'CaF2', 'CaSO4', 'CaCO3', 'BaO', 'BaSO4', 'BaCO3', 'BaSiO3', 'BaS', 'NaOH', '辉铜矿', '黄铜矿', '铜铁硫化相', '铁橄榄石', '磁铁矿', '钙铁辉石', '玻璃相', '石膏', '方解石', '石英', '砷铜矿', '皓矾', '六水锌矾', '氧化锑', '三氧化二砷', '五氧化二砷', '铅绿矾', '方铅矿', '铅黄', '铅', '密陀僧', '红锌矿', '闪锌矿', '锌', '纤锌矿', '冰晶石', '刚玉', 'β氧化铝', '钾冰晶石', '铝', '锥冰晶石', '西蒙冰晶石', '氟铝钙锂石', '白砷石', '三水胆矾', '副雄黄', '砷华', '铅矾', '块黑铅矿', '四水锌矾', '硒汞矿', '尖晶石', '氮化铝', '方镁石', '铜靛矾', 'CuSO4H2O', 'CdSO30_5H2O', '石盐', '氟氯铅矿', '铁白云石', '钙铝矾', '氯铅矿', 'T_B', 'T_Na', 'T_Mg', 'T_Al', 'T_K', 'T_Ca', 'T_Fe', 'T_Cu', 'T_Pb', 'T_Zn', 'T_Sn', 'T_Ni', 'T_Co', 'T_Sb', 'T_Hg', 'T_Cd', 'T_Bi', 'T_Cr', 'T_As', 'T_Be', 'T_Ba', 'T_Pd', 'T_Pt', 'T_V', 'T_Mn', 'T_Ti', 'T_Al3', 'T_SO42', 'CN', 'T_F', '萘', '苊烯', '苊', '芴', '菲', '蒽', '荧蒽', '芘', '苯并a蒽', '屈', '苯并b荧蒽', '苯并k荧蒽', '苯并a芘', '茚苯123_cd芘', '二苯并a_n蒽', '苯并ghi北二萘嵌苯', '乙酸乙酯', '乙酸丁酯', '乙酸异戊酯', '氨基甲酸乙酯', '邻甲酸甲酯', '邻甲基苯甲酸', '丁酸丁酯', 'N_氰基乙酰亚胺甲酯乙酯', 'T_43甲基3甲亚基氨基苯基丁酸乙酯', '氯甲酸甲酯', '邻苯二甲酸二甲酯', '邻甲基苯甲酸甲酯', '邻苯二甲酸二乙酯', '邻苯二甲酸二异丁酯', '邻苯二甲酸二正丁酯', '邻苯二甲酸二2甲氧基乙酯', '邻苯二甲酸二4甲基戊基酯', '邻苯二甲酸二2乙氧基乙酯', '邻苯二甲酸二戊酯', '邻苯二甲酸二己酯', '邻苯二甲酸丁基苄基酯', '邻苯二甲酸二2丁氧基乙酯', '邻苯二甲酸二环己酯', '邻苯二甲酸二2乙基己酯', '邻苯二甲酸二苯酯', '邻苯二甲酸二正辛酯', '邻苯二甲酸二壬酯', '苯', '甲苯', '乙苯', '二甲苯', '对二甲苯', '间二甲苯', '邻二甲苯', '异丙苯', '苯乙烯', '乙烯基甲苯', '环己烷', '二氯甲烷', '二氯乙烷', '苯酚', '邻甲酚', 'T_24二氯酚', 'T_25二氯苯酚', '甲醛', '间苯氧基苯甲醛', '甲酸', '苯氧乙酸', '氯乙酸', '羟基乙酸', 'T_2甲4氯酸', '甘氨酸', '亚磷酸钠', '甲基草甘膦酸钠盐', '羟甲基磷酸钠盐', 'T_24二氯苯氧乙酸钠', '氯甲基吡啶', '吡啶', 'T_2氯5氯甲基吡啶', '三氯吡啶醇钠', '乙基氯化物', '氯乙酰氯', '邻苯二胺', '苯肼', '脲', 'T_1苯基氨基脲', '二甲胺', 'T_2氯烟酰胺', '精胺', '胺醚', '乙撑硫脲', '邻甲基苯基硫脲', 'T_2氯N氯甲基_N26二乙基苯基乙酰胺MRM', 'N_26二乙基苯基甲亚胺甲叉', '丁草胺', 'T_4_3乙基2甲亚基氨基苯基丁酰氯', 'T_25二氯苯胺', 'T_24D', '草甘膦', '增甘膦', '双甘膦', '西玛津', '三唑磷', '烟嘧磺酰氯', '烟嘧磺胺', '烟嘧磺隆', '毒死蜱', '多菌灵', '氟乐灵', '咪鲜胺', '莠去津', '百草枯', '苯磺隆', '吡虫啉', '咪唑烷', '丙环唑', '代森锰', '敌百虫', '啶虫脒', '麦草畏', '杀虫单', '乙草胺', '溴丙烷', '四氯化碳', '丙溴磷', '对氯三氟甲苯', '功夫酰氯', '苄基三乙基氯化铵', '二氯菊酰氯', 'T_4甲基2肼基苯并骈噻唑', '苯唑醇', '二甲硫醚', '硫酸二甲酯', '甲醇', '乙醇', '辛硫磷', 'T_OO二乙基硫代磷酰氯', '醋酸', '醋酸酐', '丙烯醛', '丙烯腈', '环戊二烯', 'L_Ca', 'L_Mg', 'L_Fe', 'L_Cu', 'L_Pb', 'L_Zn', 'L_Ba', 'L_Sn', 'L_Co', 'L_Sb', 'L_Hg', 'L_Cd', 'L_Bi', 'L_Ni', 'L_Cr', 'L_Ag', 'L_As', 'L_Se', 'L_Br', 'L_V', 'L_F']
Labels = ['行业分类', '固废名称', '别名', '产生工段', '表观形貌稍微详细', '表观形貌关键词', '物理形态', '形状', '颜色', '气味', '密度', '含水率', 'pH', '含油率', 'COD', '热值', '烧失率', '水分', '灰分', '挥发分', '固定碳', 'C', 'H']

# 标签分类
basic_info = ['废物类别', '行业分类', '固废名称 ', '别名', '产生工段', '表观形貌（稍微详细）', '表观形貌关键词', '物理形态', '形状', '颜色', '气味', '密度', '含水率', 'pH', '含油率', 'COD', '热值', '烧失量']
# 工业组成分析
industrial = ['水分', '灰分', '挥发分', '固定碳']

# 元素组成
elementalComposition = ["C","H","N","O","F","Na","Mg","Al","Si","P","S","Cl","K","Ca","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
                        "As","Pb","Ag","Bi","Cd","Sn","Sb","I","Hg","Ba"]
# 物相组成
phaseComposition =['Al2O3', 'MgO', 'P_Cl', 'K2O', 'Na2O', 'Fe2O3', 'SiO2', 'MnO', 'CaO', 'P_S', 'SO3', 'As2O3', 'TiO2', 'Cr2O3', 'CuO', 'ZnO',
                    'PbO', 'P_F', 'V2O5', 'BaO', 'P2O5', 'SnO2', 'NiO', 'NaCl', 'KCl', 'MgCl2', 'MgOH2','AlCl3', 'MnCl2',
                    'NH4Cl', 'TiCl4', 'FeCl2', 'FeCl3', 'CaCl2', 'CaF2', 'CaSO4', 'CaCO3', 'P_BaO', 'BaSO4', 'BaCO3', 'BaSiO3', 'BaS', 'NaOH',
                    '辉铜矿', '黄铜矿', '铜铁硫化相', '铁橄榄石', '磁铁矿', '钙铁辉石', '玻璃相', '石膏', '方解石', '石英', '砷铜矿', '皓矾', '六水锌矾', '氧化锑', '三氧化二砷',
                    '五氧化二砷', '铅绿矾', '方铅矿', '铅黄', '铅', '密陀僧', '红锌矿', '闪锌矿', '锌', '纤锌矿', '冰晶石', '刚玉', 'β氧化铝', '钾冰晶石', '铝', '锥冰晶石',
                    '西蒙冰晶石', '氟铝钙锂石', '白砷石', '三水胆矾', '副雄黄', '砷华', '铅矾', '块黑铅矿', '四水锌矾', '硒汞矿', '尖晶石', '氮化铝', '方镁石', '铜靛矾', 'CuSO4H2O',
                    'CdSO30_5H2O', '石盐', '氟氯铅矿', '铁白云石', '钙铝矾', '氯铅矿']

# 污染物含量
pollutantContent =['T_B', 'T_Na', 'T_Mg', 'T_Al', 'T_K', 'T_Ca', 'T_Fe', 'T_Cu', 'T_Pb', 'T_Zn', 'T_Sn', 'T_Ni', 'T_Co','T_Sb', 'T_Hg', 'T_Cd', 'T_Bi', 'T_Cr',
                    'T_As', 'T_Be', 'T_Ba', 'T_Pd', 'T_Pt', 'T_V', 'T_Mn', 'T_Ti', 'T_Al3','T_SO42', 'CN', 'T_F']

# 多环芳烃
PAHs = ['萘', '苊烯', '苊', '芴', '菲', '蒽', '荧蒽', '芘', '苯并a蒽', '屈', '苯并b荧蒽', '苯并k荧蒽', '苯并a芘', '茚苯123_cd芘', '二苯并a_n蒽', '苯并ghi北二萘嵌苯']

# 有机污染物
organicPollutant = ['乙酸乙酯', '乙酸丁酯', '乙酸异戊酯', '氨基甲酸乙酯', '邻甲酸甲酯', '邻甲基苯甲酸', '丁酸丁酯', 'N_氰基乙酰亚胺甲酯乙酯', 'T_43甲基3甲亚基氨基苯基丁酸乙酯', '氯甲酸甲酯',
                    '邻苯二甲酸二甲酯', '邻甲基苯甲酸甲酯', '邻苯二甲酸二乙酯','邻苯二甲酸二异丁酯', '邻苯二甲酸二正丁酯', '邻苯二甲酸二2甲氧基乙酯', '邻苯二甲酸二4甲基戊基酯',
                    '邻苯二甲酸二2乙氧基乙酯', '邻苯二甲酸二戊酯', '邻苯二甲酸二己酯', '邻苯二甲酸丁基苄基酯', '邻苯二甲酸二2丁氧基乙酯', '邻苯二甲酸二环己酯','邻苯二甲酸二2乙基己酯',
                    '邻苯二甲酸二苯酯', '邻苯二甲酸二正辛酯', '邻苯二甲酸二壬酯', '苯', '甲苯', '乙苯', '二甲苯', '对二甲苯', '间二甲苯', '邻二甲苯', '异丙苯', '苯乙烯', '乙烯基甲苯', '环己烷',
                    '二氯甲烷', '二氯乙烷', '苯酚', '邻甲酚','T_24二氯酚', 'T_25二氯苯酚', '甲醛', '间苯氧基苯甲醛', '甲酸', '苯氧乙酸', '氯乙酸', '羟基乙酸',
                    'T_2甲4氯酸', '甘氨酸', '亚磷酸钠', '甲基草甘膦酸钠盐', '羟甲基磷酸钠盐', 'T_24二氯苯氧乙酸钠','氯甲基吡啶', '吡啶', 'T_2氯5氯甲基吡啶', '三氯吡啶醇钠',
                    '乙基氯化物', '氯乙酰氯', '邻苯二胺', '苯肼', '脲', 'T_1苯基氨基脲', '二甲胺', 'T_2氯烟酰胺', '精胺', '胺醚', '乙撑硫脲', '邻甲基苯基硫脲',
                    'T_2氯N氯甲基_N26二乙基苯基乙酰胺MRM','N_26二乙基苯基甲亚胺甲叉', '丁草胺', 'T_4_3乙基2甲亚基氨基苯基丁酰氯', 'T_25二氯苯胺']

# 农药
pesticide = ['T_24D', '草甘膦', '增甘膦', '双甘膦', '西玛津', '三唑磷', '烟嘧磺酰氯', '烟嘧磺胺', '烟嘧磺隆','毒死蜱', '多菌灵', '氟乐灵', '丁草胺', '咪鲜胺', '莠去津', '百草枯', '苯磺隆',
            '吡虫啉', '咪唑烷', '丙环唑', '代森锰', '敌百虫', '啶虫脒', '麦草畏', '杀虫单', '乙草胺', '溴丙烷', '四氯化碳', '丙溴磷', '对氯三氟甲苯','功夫酰氯', '苄基三乙基氯化铵',
            '二氯菊酰氯', 'T_4甲基2肼基苯并骈噻唑', '苯唑醇', '二甲硫醚', '硫酸二甲酯', '甲醇', '乙醇', '辛硫磷', 'T_OO二乙基硫代磷酰氯','醋酸', '醋酸酐', '丙烯醛', '丙烯腈', '环戊二烯']
# 毒性浸出浓度
toxicLeachingConcentration = ['L_Ca', 'L_Mg', 'L_Fe', 'L_Cu', 'L_Pb', 'L_Zn', 'L_Ba', 'L_Sn', 'L_Co', 'L_Sb', 'L_Hg', 'L_Cd', 'L_Bi', 'L_Ni', 'L_Cr', 'L_Ag', 'L_As','L_Se', 'L_Br', 'L_V', 'L_F']


def wasteList(request):


    """ 搜索 """
    data_dict = {}
    search_data = request.GET.get('q',"")
    if search_data:
        data_dict["固废名称__contains"] = search_data

    """根据搜索条件 获取用户列表"""
    queryset = models.WasteInfo.objects.filter(**data_dict)
    print("queryset", queryset)
    # for obj in queryset:
    #     for i in obj.objects:
    #         print(i)


    """分页内容"""
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
        'labels': labels,
    }
    return render(request, 'wasteList.html', context)

def wasteAdd(request):

    title = "废物数据管理——新增废物"

    context = {
        'elementLabels': elementalComposition,
        'phaseLabels': phaseComposition,
        'pollutantLabels': pollutantContent,
        'PAHs': PAHs,
        'organic': organicPollutant,
        'pesticide': pesticide,
        'toxicLabels': toxicLeachingConcentration,
        'title': title,
    }

    if request.method == "GET":
        return render(request, 'waste_Add.html',context)

    # 获取用户提交数据

    废物类别 = request.POST.get('废物类别')
    print("废物类别",废物类别)
    行业分类 = request.POST.get('行业分类')
    固废名称 = request.POST.get('固废名称')
    产生工段 = request.POST.get('产生工段')
    表观形貌稍微详细 = request.POST.get('表观形貌')
    物理形态 = request.POST.get('物理形态')
    形状 = request.POST.get('形状')
    颜色 = request.POST.get('颜色')
    气味 = request.POST.get('气味')
    密度 = request.POST.get('密度')
    含水率 = request.POST.get('含水率')
    pH = request.POST.get('pH')
    水分 = request.POST.get('水分')
    灰分 = request.POST.get('灰分')
    挥发分 = request.POST.get('挥发分')
    固定碳 = request.POST.get('固定碳')
    label_list = ['废物类别', '行业分类', '固废名称','产生工段', '表观形貌稍微详细', '物理形态', '形状', '颜色', '气味', '密度', '含水率','烧失量', '水分', '灰分', '挥发分', '固定碳']
    item_list = [废物类别, 行业分类, 固废名称, 产生工段, 表观形貌稍微详细, 物理形态, 形状, 颜色, 气味, 密度, 含水率, pH, 水分, 灰分, 挥发分, 固定碳]
    partial_item = dict(zip(label_list, item_list))
    #print("partial_item",partial_item)


    labels = request.POST.getlist('LabelName')
    print("labels",labels)
    inputs = request.POST.getlist('q')
    # units = request.POST.getlist('unitName')
    # print("units", units)
    waste_item = dict(zip(labels, inputs))
    for key in partial_item:
        if partial_item[key] != '':
            waste_item[key] = partial_item[key]
    for k in list(waste_item.keys()):
        if not waste_item[k]:
            del waste_item[k]
    #print('waste_item', waste_item)
    waste_file = request.FILES
    print('waste_file', waste_file)

    if waste_item == {}:
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
            wasteName=固废名称,
            img=file_path,
        )
        return render(request, "fileLoad.html", context)

    # 处理废物新增
    newId = models.WasteInfo.objects.last().dataId + 1
    models.WasteInfo.objects.create(dataId=newId)
    models.WasteInfo.objects.filter(dataId=newId).update(**waste_item)

    print("成功导入数据库")

    return render(request, "wasteAdd_success.html", context)

def wasteDelete(request, nid):
    """删除废物"""
    models.WasteInfo.objects.filter(dataId=nid).delete()
    return redirect('/waste/list/')


from django import forms
# 元素组成form1
class WasteModelForm1(BootStrapModelForm):
    class Meta:
        model = models.WasteInfo
        fields = elementalComposition

# 物相组成form2
class WasteModelForm2(BootStrapModelForm):
    class Meta:
        model = models.WasteInfo
        fields = phaseComposition

# 无机元素含量
class WasteModelForm3(BootStrapModelForm):
    class Meta:
        model = models.WasteInfo
        fields = pollutantContent
# 多环芳烃
class WasteModelForm4(BootStrapModelForm):
    class Meta:
        model = models.WasteInfo
        fields = PAHs
# 有机污染物
class WasteModelForm5(BootStrapModelForm):
    class Meta:
        model = models.WasteInfo
        fields = organicPollutant
# 农药
class WasteModelForm6(BootStrapModelForm):
    class Meta:
        model = models.WasteInfo
        fields = pesticide
# 重金属毒性浸出浓度
class WasteModelForm7(BootStrapModelForm):
    class Meta:
        model = models.WasteInfo
        fields = toxicLeachingConcentration

def wasteEdit(request, nid):
    #是否能获得当前对象
    row_object = models.WasteInfo.objects.filter(dataId=nid).first()
    if not row_object:
        return redirect('/waste/list/')


    固废名称 = row_object.固废名称
    废物类别 = row_object.废物类别
    行业分类 = row_object.行业分类
    产生工段 = row_object.产生工段
    表观形貌稍微详细 = row_object.表观形貌稍微详细
    物理形态 = row_object.物理形态
    形状 = row_object.形状
    颜色 = row_object.颜色
    气味 = row_object.气味
    密度 = row_object.密度
    含水率 = row_object.含水率
    pH = row_object.pH
    水分 = row_object.水分
    灰分 = row_object.灰分
    挥发分 = row_object.挥发分
    固定碳 = row_object.固定碳
    title = "废物数据管理："
    print("固废名称", 固废名称)
    if 固废名称 == None:
        固废名称=""
    title += 固废名称
    title += "——数据修改"

    # 获取元素组成



    # 获取物相组成



    # 获取无机元素含量

    # 获取多环芳烃

    # 获取
    form1 = WasteModelForm1(instance=row_object)
    form2 = WasteModelForm2(instance=row_object)
    form3 = WasteModelForm3(instance=row_object)
    form4 = WasteModelForm4(instance=row_object)
    form5 = WasteModelForm5(instance=row_object)
    form6 = WasteModelForm6(instance=row_object)
    form7 = WasteModelForm7(instance=row_object)
    context = {
        "title": title,
        "固废名称": 固废名称,
        "废物类别": 废物类别,
        "行业分类": 行业分类,
        "产生工段": 产生工段,
        "表观形貌稍微详细": 表观形貌稍微详细,
        "物理形态": 物理形态,
        "形状": 形状,
        "颜色": 颜色,
        "气味": 气味,
        "密度": 密度,
        "含水率": 含水率,
        "pH": pH,
        "水分" :水分,
        "灰分" :灰分,
        "挥发分":挥发分,
        "固定碳" :固定碳,
        'elementLabels': elementalComposition,
        'phaseLabels': phaseComposition,
        'pollutantLabels': pollutantContent,
        'PAHs': PAHs,
        'organic': organicPollutant,
        'pesticide': pesticide,
        'toxicLabels': toxicLeachingConcentration,
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'form5': form5,
        'form6': form6,
        'form7': form7,
    }

    if request.method == "GET":
        print(row_object)
        return render(request, "wasteEdit.html", context)

    form1 = WasteModelForm1(data=request.POST, instance=row_object)
    form2 = WasteModelForm2(data=request.POST, instance=row_object)
    form3 = WasteModelForm3(data=request.POST, instance=row_object)
    form4 = WasteModelForm4(data=request.POST, instance=row_object)
    form5 = WasteModelForm5(data=request.POST, instance=row_object)
    form6 = WasteModelForm6(data=request.POST, instance=row_object)
    form7 = WasteModelForm7(data=request.POST, instance=row_object)


    废物类别1 = request.POST.get('废物类别')
    行业分类1 = request.POST.get('行业分类')
    固废名称1 = request.POST.get('固废名称')
    产生工段1 = request.POST.get('产生工段')
    表观形貌稍微详细1 = request.POST.get('表观形貌')
    物理形态1 = request.POST.get('物理形态')
    形状1 = request.POST.get('形状')
    颜色1 = request.POST.get('颜色')
    气味1 = request.POST.get('气味')
    密度1 = request.POST.get('密度')
    含水率1 = request.POST.get('含水率')
    pH1 = request.POST.get('pH')
    水分1 = request.POST.get('水分')
    灰分1 = request.POST.get('灰分')
    挥发分1 = request.POST.get('挥发分')
    固定碳1 = request.POST.get('固定碳')
    label_list = ['废物类别', '行业分类', '固废名称', '产生工段', '表观形貌稍微详细', '物理形态', '形状', '颜色',
                  '气味', '密度', '含水率', '烧失率', '水分', '灰分', '挥发分', '固定碳']
    item_list = [废物类别1, 行业分类1, 固废名称1, 产生工段1, 表观形貌稍微详细1, 物理形态1, 形状1, 颜色1, 气味1, 密度1, 含水率1, pH1,
                 水分1, 灰分1, 挥发分1, 固定碳1]
    partial_item = dict(zip(label_list, item_list))

    labels = request.POST.getlist('LabelName')
    inputs = request.POST.getlist('q')

    waste_item = dict(zip(labels, inputs))
    for key in partial_item:
        if partial_item[key] != '':
            waste_item[key] = partial_item[key]
    for k in list(waste_item.keys()):
        if not waste_item[k]:
            del waste_item[k]
    print("EDIT_waste_item",waste_item)
    if waste_item == {}:
        return render(request, "wasteEdit.html", context)

    # 更新数据库
    models.WasteInfo.objects.filter(dataId=nid).update(**waste_item)
    form1.save()
    form2.save()
    form3.save()
    form4.save()
    form5.save()
    form6.save()
    form7.save()
    return redirect('/waste/list/')









