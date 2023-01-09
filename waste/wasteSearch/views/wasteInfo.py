import csv
import os
# from waste import wasteSearch
from waste.settings import BASE_DIR
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from wasteSearch.models import WasteInfo
from wasteSearch import models
from wasteSearch.utils.pagination import Pagination
from django.apps import apps
from wasteSearch.utils import Searching5
from wasteSearch.utils import getData
from wasteSearch.utils import FunctionLearning
from django.db.models import Q
from django import forms
from wasteSearch.utils.createImage import check_code


# 无用数据项
useless_label= ["_state","id", "序号","dataId"]
# 文本描述型
text_label = ["固废名称","行业分类","废物类别","别名","产生工段","废物描述","物理形态","形状","表观形貌关键词","颜色","气味","物质组成特性","表观形貌(稍微详细)"]

basic_data_label = ["含水率(%)", "密度(kg/m3)", "热值(KJ/kg)", "含油率(%)","pH","COD(mg/L)","烧失率(%)"]

# 工业组成分析
industriolComposition = ['水分', '灰分', '挥发分', '固定碳']

# 元素组成
elementalComposition = ["C","H","N","O","F","Na","Mg","Al","Si","P","S","Cl","K","Ca","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
                        "As","Pb","Ag","Bi","Cd","Sn","Sb","I","Hg","Ba"]

# 物相组成
phaseComposition =['Al2O3', 'MgO', 'P Cl', 'K2O', 'Na2O', 'Fe2O3', 'SiO2', 'MnO', 'CaO', 'P S', 'SO3', 'As2O3', 'TiO2', 'Cr2O3', 'CuO', 'ZnO',
                    'PbO', 'P F', 'V2O5', 'BaO', 'P2O5', 'SnO2', 'NiO', 'NaCl', 'KCl', 'MgCl2', 'Mg(OH)2','AlCl3', 'MnCl2',
                    'NH4Cl', 'TiCl4', 'FeCl2', 'FeCl3', 'CaCl2', 'CaF2', 'CaSO4', 'CaCO3', 'P BaO', 'BaSO4', 'BaCO3', 'BaSiO3', 'BaS', 'NaOH',
                    '辉铜矿', '黄铜矿', '铜铁硫化相', '铁橄榄石', '磁铁矿', '钙铁辉石', '玻璃相', '石膏', '方解石', '石英', '砷铜矿', '皓矾', '六水锌矾', '氧化锑', '三氧化二砷',
                    '五氧化二砷', '铅绿矾', '方铅矿', '铅黄', '铅', '密陀僧', '红锌矿', '闪锌矿', '锌', '纤锌矿', '冰晶石', '刚玉', 'β-氧化铝', '钾冰晶石', '铝', '锥冰晶石',
                    '西蒙冰晶石', '氟铝钙锂石', '白砷石', '三水胆矾', '副雄黄', '砷华', '铅矾', '块黑铅矿', '四水锌矾', '硒汞矿', '尖晶石', '氮化铝', '方镁石', '铜靛矾', 'CuSO4•H2O',
                    'CdSO3•0.5H2O', '石盐', '氟氯铅矿', '铁白云石', '钙铝矾', '氯铅矿']

# 污染物含量
pollutantContent =['T B', 'T Na', 'T Mg', 'T Al', 'T K', 'T Ca', 'T Fe', 'T Cu', 'T Pb', 'T Zn', 'T Sn', 'T Ni', 'T Co','T Sb', 'T Hg', 'T Cd', 'T Bi', 'T Cr', 
                    'T As', 'T Be', 'T Ba', 'T Pd', 'T Pt', 'T V', 'T Mn', 'T Ti', 'T Al3+','T SO42-', 'CN', 'T F']

# 多环芳烃
PAHs = ['萘', '苊烯', '苊', '芴', '菲', '蒽', '荧蒽', '芘', '苯并（a）蒽', '屈', '苯并（b）荧蒽', '苯并 (k)荧蒽', '苯并（a）芘', '茚苯（1,2,3-cd）芘', '二苯并（a, n）蒽', '苯并（ghi）北（二萘嵌苯）']

# 有机污染物
organicPollutant = ['乙酸乙酯', '乙酸丁酯', '乙酸异戊酯', '氨基甲酸乙酯', '邻甲酸甲酯', '邻甲基苯甲酸', '丁酸丁酯', 'N-氰基乙酰亚胺甲酯（乙酯）', '4-[3-甲基-3-(（甲亚基氨基)）苯基]丁酸乙酯', '氯甲酸甲酯', 
                    '邻苯二甲酸二甲酯', '邻甲基苯甲酸甲酯', '邻苯二甲酸二乙酯','邻苯二甲酸二异丁酯', '邻苯二甲酸二正丁酯', '邻苯二甲酸二(2-甲氧基)乙酯', '邻苯二甲酸二(4-甲基-2-戊基)酯', 
                    '邻苯二甲酸二(2-乙氧基)乙酯', '邻苯二甲酸二戊酯', '邻苯二甲酸二己酯', '邻苯二甲酸丁基苄基酯', '邻苯二甲酸二(2-丁氧基)乙酯', '邻苯二甲酸二环己酯','邻苯二甲酸二（2-乙基）己酯', 
                    '邻苯二甲酸二苯酯', '邻苯二甲酸二正辛酯', '邻苯二甲酸二壬酯', '苯', '甲苯', '乙苯', '二甲苯', '对二甲苯', '间二甲苯', '邻二甲苯', '异丙苯', '苯乙烯', '乙烯基甲苯', '环己烷', 
                    '二氯甲烷', '二氯乙烷', '苯酚', '邻甲酚','2,4-二氯酚', '2,5-二氯苯酚', '甲醛', '间苯氧基苯甲醛', '甲酸', '苯氧乙酸', '氯乙酸', '羟基乙酸', 
                    '2甲4氯酸', '甘氨酸', '亚磷酸钠', '甲基草甘膦酸钠盐', '羟甲基磷酸钠盐', '2,4-二氯苯氧乙酸钠','氯甲基吡啶', '吡啶', '2-氯-5-氯甲基吡啶', '三氯吡啶醇钠', 
                    '乙基氯化物', '氯乙酰氯', '邻苯二胺', '苯肼', '脲', '1-苯基氨基脲', '二甲胺', '2-氯烟酰胺', '精胺', '胺醚', '乙撑硫脲', '邻甲基苯基硫脲', 
                    '2-氯-N-(氯甲基)-N-(2,6-二乙基苯基)乙酰胺（MRM）','N-2,6-二乙基苯基甲亚胺（甲叉）', '丁草胺', '4-[3-乙基-2-(甲亚基氨基)苯基]丁酰氯', '2,5-二氯苯胺']

# 农药
pesticide = ['2,4-D', '草甘膦', '增甘膦', '双甘膦', '西玛津', '三唑磷', '烟嘧磺酰氯', '烟嘧磺胺', '烟嘧磺隆(mg/kg)','毒死蜱', '多菌灵', '氟乐灵', '丁草胺', '咪鲜胺', '莠去津', '百草枯', '苯磺隆', 
            '吡虫啉', '咪唑（烷）', '丙环唑', '代森锰', '敌百虫', '啶虫脒', '麦草畏', '杀虫单', '乙草胺', '溴丙烷', '四氯化碳', '丙溴磷', '对氯三氟甲苯','功夫酰氯', '苄基三乙基氯化铵',
            '二氯菊酰氯', '4-甲基-2-肼基苯并骈噻唑', '苯唑醇', '二甲硫醚', '硫酸二甲酯', '甲醇', '乙醇', '辛硫磷', 'O,O-二乙基硫代磷酰氯','醋酸', '醋酸酐', '丙烯醛', '丙烯腈', '环戊二烯']
# 毒性浸出浓度
toxicLeachingConcentration = ['L Ca', 'L Mg', 'L Fe', 'L Cu', 'L Pb', 'L Zn', 'L Ba', 'L Sn', 'L Co', 'L Sb', 'L Hg', 'L Cd', 'L Bi', 'L Ni', 'L Cr', 'L Ag', 'L As','L Se', 'L Br', 'L V', 'L F']


physical_solid=["表观形貌","颜色","气味","含水率(%)","密度(kg/m3)","含油率(%)"]
physical_halfsolid=["表观形貌","颜色","气味","含水率(%)","密度(kg/m3)","含油率(%)"]
physical_liquid=["颜色","气味","密度","含油率(%)"]
chemical_solid=["工业组成","元素组成","物相组成","污染物含量","毒性浸出浓度","有机污染物","多环芳烃","农药"]
chemical_halfsolid=["工业组成","元素组成","物相组成","污染物含量","毒性浸出浓度","有机污染物","多环芳烃","农药"]
chemical_liquid=["工业组成","元素组成","污染物含量","毒性浸出浓度","有机污染物","多环芳烃","农药"]


# Create your views here.
def index(request):
    # 获取用户提交过来的数据
    search_data = request.GET.get('q', "")

    queryset = getData.searchByName(search_data)
    res_dict = []
    for obj in queryset:
        name = obj.固废名称
        flag = True
        obj_dict = obj.__dict__
        for dict_item in res_dict:
            if dict_item["固废名称"] == name:
                flag = False
                index = res_dict.index(dict_item)
                for item in obj_dict:
                    if (item in useless_label) | (item in text_label):
                        continue
                    else :
                        if obj_dict[item]:
                            if item not in res_dict[index]:
                                res_dict[index][item] = [obj_dict[item]]
                            else:
                                res_dict[index][item].append(obj_dict[item])
                break
        
        if flag:
            res_dict.append({"固废名称": name})
            index = res_dict.index({"固废名称": name})
            # print(res_dict[index][name])
            for item in obj_dict:
                if item in useless_label:
                    continue
                if obj_dict[item]:
                    if item in text_label:
                        res_dict[index][item] = obj_dict[item]
                    else:
                        res_dict[index][item] = [obj_dict[item]]

    # print(res_dict)        
    # 分页
    page_object = Pagination(request, res_dict, 15)
    # page_object = Pagination(request, queryset, 15)

    modelobj = apps.get_model('wasteSearch.WasteInfo')
    field_dic=[]
    for field in modelobj._meta.fields:
        field_dic.append(field.verbose_name)
    
    wasteType = {}
    names = []
    category = {}
    for item in models.WasteInfo.objects.all():
        name = item.固废名称
        if name != None:
            if name not in names:
                # 计算废物类别
                if item.废物类别 != None:
                    if item.废物类别 in wasteType:
                        wasteType[item.废物类别] += 1
                    else:
                        wasteType[item.废物类别] = 1
                # 统计行业分类
                if item.行业分类 != None:
                    if item.行业分类 in category:
                        category[item.行业分类] += 1
                    else:
                        category[item.行业分类] = 1
                names.append(name)
    
    waste_type = []
    waste_dict = {}
    for key in wasteType:
        waste_dict['value'] = wasteType[key]
        waste_dict['name'] = key
        waste_type.append(waste_dict)
        waste_dict = {}
    
    category_name = []
    category_data = []
    for key in category:
        category_name.append(key)
        category_data.append(category[key])

    numOfWaste = len(names)
    keywords = []
    keywords.append({"name":str(numOfWaste)+"种","value":numOfWaste})
    # print("waste_type", waste_type)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 页码
        "field_dic": field_dic,
        "waste_type": waste_type,
        "category_name": category_name,
        "category_data": category_data,
        "keywords": keywords
    }
    return render(request, 'index.html', context)

def details(request, name):

    # name2verboseName = {}
    # fields = apps.get_model('wasteSearch.WasteInfo')._meta.fields
    # # 建立models中存储的表名还原
    # for item in fields:
    #     name2verboseName[item.name] = item.verbose_name

    basic_info = getData.getBasicInfo(name, text_label, basic_data_label)

    names = []
    for item in models.WasteInfo.objects.all():
        n = item.固废名称
        if n != None:
            if n not in names:
                names.append(n)
    names.sort()

    # 元素组成 箱线图
    element3, element5, element10, element_txt, element_size = getData.buildDetailsInfo_boxplot(name, elementalComposition)
    # 物相组成 箱线图
    phase3, phase5, phase10, phase_txt, phase_size = getData.buildDetailsInfo_boxplot(name, phaseComposition)
    # 污染物含量
    polluCont3, polluCont5, polluCont10, polluCont_txt, polluCont_size= getData.buildDetailsInfo_boxplot(name, pollutantContent)
    # 多环芳烃 
    PAH3, PAH5, PAH10, PAH_txt, PAH_size= getData.buildDetailsInfo_boxplot(name, PAHs)
    # 毒性浸出液 柱状图
    toxic3, toxic5, toxic10, toxic_txt, toxic_size= getData.buildDetailsInfo_boxplot(name, toxicLeachingConcentration)
    # 有机污染物
    organic3, organic5, organic10, organic_txt, organic_size= getData.buildDetailsInfo_boxplot(name, organicPollutant)
    # 农药
    pesticide3, pesticide5, pesticide10, pesticide_txt, pesticide_size= getData.buildDetailsInfo_boxplot(name, pesticide)

    context = {
        "currname": name,
        "names": names,
        "basic_info": basic_info,
        "element3": element3,
        "element5": element5,
        "element10": element10,
        "element_txt": element_txt,
        "element_size": max(element_size,1)+1,
        "phase3": phase3,
        "phase5": phase5,
        "phase10": phase10,
        "phase_txt": phase_txt,
        "phase_size": max(phase_size,1)+1,
        "polluCont3": polluCont3,
        "polluCont5": polluCont5,
        "polluCont10": polluCont10,
        "polluCont_txt": polluCont_txt,
        "polluCont_size": max(polluCont_size,1)+1,
        "PAH3": PAH3,
        "PAH5": PAH5,
        "PAH10": PAH10,
        "PAH_txt": PAH_txt,
        "PAH_size": max(PAH_size,1)+1,
        "toxic3": toxic3,
        "toxic5": toxic5,
        "toxic10": toxic10,
        "toxic_txt": toxic_txt,
        "toxic_size": max(toxic_size,1)+1,
        "organic3": organic3,
        "organic5": organic5,
        "organic10": organic10,
        "organic_txt": organic_txt,
        "organic_size": max(organic_size,1)+1,
        "pesticide3": pesticide3,
        "pesticide5": pesticide5,
        "pesticide10": pesticide10,
        "pesticide_txt": pesticide_txt,
        "pesticide_size": max(pesticide_size,1)+1,
    }

    return render(request, 'details.html', context)

def compare(request, name, comparename):

    basic_info = getData.getBasicInfo(name, text_label, basic_data_label)
    basic_info_com = getData.getBasicInfo(comparename, text_label, basic_data_label)

    names = []
    for item in models.WasteInfo.objects.all():
        n = item.固废名称
        if n != None:
            if n not in names:
                names.append(n)
    names.sort()

    # 元素组成 箱线图
    element3, element5, element10, element_txt, element_size = getData.buildDetailsInfo_boxplot(name, elementalComposition)
    element3_com, element5_com, element10_com, element_txt_com, element_size_com = getData.buildDetailsInfo_boxplot(comparename, elementalComposition)
    # 物相组成 箱线图
    phase3, phase5, phase10, phase_txt, phase_size = getData.buildDetailsInfo_boxplot(name, phaseComposition)
    phase3_com, phase5_com, phase10_com, phase_txt_com, phase_size_com = getData.buildDetailsInfo_boxplot(comparename, phaseComposition)
    # 污染物含量
    polluCont3, polluCont5, polluCont10, polluCont_txt, polluCont_size= getData.buildDetailsInfo_boxplot(name, pollutantContent)
    polluCont3_com, polluCont5_com, polluCont10_com, polluCont_txt_com, polluCont_size_com= getData.buildDetailsInfo_boxplot(comparename, pollutantContent)
    # 多环芳烃 
    PAH3, PAH5, PAH10, PAH_txt, PAH_size= getData.buildDetailsInfo_boxplot(name, PAHs)
    PAH3_com, PAH5_com, PAH10_com, PAH_txt_com, PAH_size_com= getData.buildDetailsInfo_boxplot(comparename, PAHs)
    # 毒性浸出液 柱状图
    toxic3, toxic5, toxic10, toxic_txt, toxic_size= getData.buildDetailsInfo_boxplot(name, toxicLeachingConcentration)
    toxic3_com, toxic5_com, toxic10_com, toxic_txt_com, toxic_size_com= getData.buildDetailsInfo_boxplot(comparename, toxicLeachingConcentration)
    # 有机污染物
    organic3, organic5, organic10, organic_txt, organic_size= getData.buildDetailsInfo_boxplot(name, organicPollutant)
    organic3_com, organic5_com, organic10_com, organic_txt_com, organic_size_com= getData.buildDetailsInfo_boxplot(comparename, organicPollutant)
    # 农药
    pesticide3, pesticide5, pesticide10, pesticide_txt, pesticide_size= getData.buildDetailsInfo_boxplot(name, pesticide)
    pesticide3_com, pesticide5_com, pesticide10_com, pesticide_txt_com, pesticide_size_com= getData.buildDetailsInfo_boxplot(comparename, pesticide)

    context = {
        "currname": name,
        "comparename": comparename,
        "names": names,
        "basic_info": basic_info,
        "element3": element3,
        "element5": element5,
        "element10": element10,
        "element_txt": element_txt,
        "element_size": max(element_size,1)+1,
        "phase3": phase3,
        "phase5": phase5,
        "phase10": phase10,
        "phase_txt": phase_txt,
        "phase_size": max(phase_size,1)+1,
        "polluCont3": polluCont3,
        "polluCont5": polluCont5,
        "polluCont10": polluCont10,
        "polluCont_txt": polluCont_txt,
        "polluCont_size": max(polluCont_size,1)+1,
        "PAH3": PAH3,
        "PAH5": PAH5,
        "PAH10": PAH10,
        "PAH_txt": PAH_txt,
        "PAH_size": max(PAH_size,1)+1,
        "toxic3": toxic3,
        "toxic5": toxic5,
        "toxic10": toxic10,
        "toxic_txt": toxic_txt,
        "toxic_size": max(toxic_size,1)+1,
        "organic3": organic3,
        "organic5": organic5,
        "organic10": organic10,
        "organic_txt": organic_txt,
        "organic_size": max(organic_size,1)+1,
        "pesticide3": pesticide3,
        "pesticide5": pesticide5,
        "pesticide10": pesticide10,
        "pesticide_txt": pesticide_txt,
        "pesticide_size": max(pesticide_size,1)+1,

        "basic_info_com": basic_info_com,
        "element3_com": element3_com,
        "element5_com": element5_com,
        "element10_com": element10_com,
        "element_txt_com": element_txt_com,
        "element_size_com": max(element_size_com,1)+1,
        "phase3_com": phase3_com,
        "phase5_com": phase5_com,
        "phase10_com": phase10_com,
        "phase_txt_com": phase_txt_com,
        "phase_size_com": max(phase_size_com,1)+1,
        "polluCont3_com": polluCont3_com,
        "polluCont5_com": polluCont5_com,
        "polluCont10_com": polluCont10_com,
        "polluCont_txt_com": polluCont_txt_com,
        "polluCont_size_com": max(polluCont_size_com,1)+1,
        "PAH3_com": PAH3_com,
        "PAH5_com": PAH5_com,
        "PAH10_com": PAH10_com,
        "PAH_txt_com": PAH_txt_com,
        "PAH_size_com": max(PAH_size_com,1)+1,
        "toxic3_com": toxic3_com,
        "toxic5_com": toxic5_com,
        "toxic10_com": toxic10_com,
        "toxic_txt_com": toxic_txt_com,
        "toxic_size_com": max(toxic_size_com,1)+1,
        "organic3_com": organic3_com,
        "organic5_com": organic5_com,
        "organic10_com": organic10_com,
        "organic_txt_com": organic_txt_com,
        "organic_size_com": max(organic_size_com,1)+1,
        "pesticide3_com": pesticide3_com,
        "pesticide5_com": pesticide5_com,
        "pesticide10_com": pesticide10_com,
        "pesticide_txt_com": pesticide_txt_com,
        "pesticide_size_com": max(pesticide_size_com,1)+1,
    }

    return render(request, 'compare.html', context)

# 数据初始化导入数据库及统计每一类数据范围
def create(request):
    queryset = WasteInfo.objects.all()
    file_path = os.path.join(BASE_DIR,'wasteSearch/files/')
    csv_path = "%s%s" % (file_path, "六行业汇总-12.23.csv")
    csv_file = open(csv_path, encoding='utf-8')
    csv_reader_lines = csv.reader(csv_file)
    labels = []
    names = apps.get_model('wasteSearch.WasteInfo')._meta.fields
    #print('names', len(names))
    for name in names:
        labels.append(name.name)
        # print(name.name)
    for index, i in enumerate(csv_reader_lines):
        if index <= 1:
            continue
        dict = {}
        num = 0
        #print('labels',len(labels))
        for data in i:
            num += 1
            #print('num', num)
            if data:
                #print(data)
                dict[labels[num]] = data
        #print(index)
        dict['dataId'] = index - 1
        # print(dict)
        WasteInfo.objects.create(**dict)
    
    return HttpResponse("数据库导入成功")


def search_modelchoice(request):
    models=["匹配度模型","废物产生节点溯源","固相热处理渣类废物溯源","浸出渣类废物溯源","精蒸馏残渣类废物溯源","收尘灰类废物溯源模型1","收尘灰类废物溯源模型2","铝灰溯源判别模型","表面处理污泥溯源判别模型"]
    context = {
        "models": models
    }
    return render(request, 'search_modelchoice.html', context)


def search_model(request, modelname):
    models=["匹配度模型","废物产生节点溯源","固相热处理渣类废物溯源","浸出渣类废物溯源","精蒸馏残渣类废物溯源","收尘灰类废物溯源模型1","收尘灰类废物溯源模型2","铝灰溯源判别模型","表面处理污泥溯源判别模型"]
    modelaccuracy = {"废物产生节点溯源":'86%',"固相热处理渣类废物溯源":'92%',"浸出渣类废物溯源":'63%',"精蒸馏残渣类废物溯源":'58%',"收尘灰类废物溯源模型1":"82%","收尘灰类废物溯源模型2":"100%"}
    labels = []
    modeldetails = ""
    if modelname == "废物产生节点溯源":
        labels = ["表观形貌", "物理形态", "含水率"]
        modeldetails="“废物产生节点溯源”通过一级指纹来预测该废物的种类，该模型使用的一级指纹包括：表观形貌、物理形态、含水率，可以预测的种类包括：固相热处理渣、液固相浸出渣、液相反应残液、蒸馏精馏、收尘灰、蒸发结晶、废水处理污泥。"
    elif modelname == "固相热处理渣类废物溯源":
        labels = ["Fe", "Cu", "Zn", "Al2O3", "MgO", "Fe2O3", "SiO2", "CaO", "PbO", "BaO"]
        modeldetails="“固相热处理渣类废物溯源”通过二级指纹来预测废物的名称，使用时请确保废物所属种类是固相热处理渣，该模型使用的二级指纹包括：Fe、Cu、Zn、Al2O3、MgO、Fe2O3、SiO2、CaO、PbO、BaO。"
    elif modelname == "收尘灰类废物溯源模型1":
        labels = ["Zn", "Pb", "Al2O3", "P Cl", "Fe2O3", "SiO2", "CaO"]
        modeldetails="“收尘灰类废物溯源模型1”通过二级指纹来预测废物的名称，使用时请确保废物所属种类是收尘灰，该模型使用的二级指纹包括：Zn、Pb、Al2O3、P Cl、Fe2O3、SiO2、CaO。"
    elif modelname == "收尘灰类废物溯源模型2":
        labels = ["T Cu", "T Pb", "T Zn", "T Ni", "T Cr", "T As", "T Ba"]
        modeldetails="“收尘灰类废物溯源模型2”通过三级指纹来预测废物的名称，使用时请确保废物所属种类是收尘灰，该模型使用的三级指纹包括：T Cu、T Pb、T Zn、T Ni、T Cr、T As、T Ba。"
    elif modelname == "浸出渣类废物溯源":
        labels = ["Cr", "Ni", "Cu", "Zn", "Al2O3", "MgO", "Fe2O3", "SiO2", "MnO", "CaO", "TiO2"]
        modeldetails="“浸出渣类废物溯源”通过二级指纹来预测废物的名称，使用时请确保废物所属种类是液固相浸出渣，该模型使用的二级指纹包括：Cr、Ni、Cu、Zn、Al2O3、MgO、Fe2O3、SiO2、MnO、CaO、TiO2。"
    elif modelname == "精蒸馏残渣类废物溯源":
        labels = ["灰分", "挥发分", "C", "H", "O"]
        modeldetails="“精蒸馏残渣类废物溯源”通过二级指纹来预测废物的名称，使用时请确保废物所属种类是蒸馏精馏，该模型使用的二级指纹包括：灰分、挥发分、C、H、O。"
    elif modelname == "铝灰溯源判别模型":
        labels = ["Al2O3", "Al", "AlN","F"]
        modeldetails="铝灰溯源判别模型,铝灰指标Al、Al2O3、AlN、F及其相对含量构成铝灰基本特征,测定四种物质（Al、Al2O3、AlN、F）相对含量，判断其含量是否落在闭合区间内."
    elif modelname == "表面处理污泥溯源判别模型":
        labels = ["SnO2","CuO","Cr2O3","NiO","ZnO"]
        modeldetails="表面处理污泥溯源判别模型，表面处理污泥中重要成分为SnO2、CuO、Cr2O3、NiO、ZnO，为表面处理污泥的指纹指标，五种物质在表面处理污泥中存在一定的数量关系。"

    values = request.GET.getlist('labelValue')
    lableAndvalues = {}
    for label, value in zip(labels,values):
        lableAndvalues[label] = value
    # print(lableAndvalues)
    result = ''
    if len(values):
        result = FunctionLearning.searchByModel(modelname,lableAndvalues)
        
    queryset = WasteInfo.objects.filter(固废名称=result)

    res_dict = []
    for obj in queryset:
        name = obj.固废名称
        flag = True
        obj_dict = obj.__dict__
        for dict_item in res_dict:
            if dict_item["固废名称"] == name:
                flag = False
                index = res_dict.index(dict_item)
                for item in obj_dict:
                    if (item in useless_label) | (item in text_label):
                        continue
                    else :
                        if obj_dict[item]:
                            if item not in res_dict[index]:
                                res_dict[index][item] = [obj_dict[item]]
                            else:
                                res_dict[index][item].append(obj_dict[item])
                break
        
        if flag:
            res_dict.append({"固废名称": name})
            index = res_dict.index({"固废名称": name})
            # print(res_dict[index][name])
            for item in obj_dict:
                if item in useless_label:
                    continue
                if obj_dict[item]:
                    if item in text_label:
                        res_dict[index][item] = obj_dict[item]
                    else:
                        res_dict[index][item] = [obj_dict[item]]
    if (modelname != "废物产生节点溯源") and (modelname != "铝灰溯源判别模型") and (modelname != "表面处理污泥溯源判别模型"):
        for item in res_dict:
            item["匹配度"] = modelaccuracy[modelname]
    page_object = Pagination(request, res_dict, 15)
    # print(lableAndvalues)
    context = {
        "modelname": modelname,
        "labels": labels,
        "models": models,
        "modeldetails": modeldetails,
        "result": result,
        "search_dict": lableAndvalues,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 页码
    }
    if lableAndvalues:
        if modelname == "废物产生节点溯源":
            return render(request, 'search_model_res_class.html', context)
        elif modelname == "铝灰溯源判别模型":
            return render(request, 'search_model_res_Al.html', context)
        elif modelname == "表面处理污泥溯源判别模型":
            return render(request, 'search_model_res_surface.html', context)
        else:
            return render(request, 'search_res.html', context)
    return render(request, 'search_model.html', context)

def search_label(request):
    physicalForm = request.GET.get('physicalform', "")
    shape = request.GET.get('shape', "")
    pH = request.GET.get('pH', "")
    # toc = request.GET.get('TOC(%)', "")
    cod = request.GET.get('COD(mg/L)', "")
    heat = request.GET.get('热值(MJ/kg)', "")

    physicalNames = request.GET.getlist('physicalName')
    physicalValues = request.GET.getlist('physicalValue', "")

    # modelobj = apps.get_model('wasteSearch.WasteInfo')
    # field_dic=[]

    # for field in modelobj._meta.fields:
    #     name = field.verbose_name
    #     field_dic.append(field.name)
    chemicalClass = request.GET.getlist('chemicalClass')
    chemicalNames = request.GET.getlist('chemicalName')
    chemicalValues = request.GET.getlist('chemicalValue')

    # 整理用户输入的标签信息
    search_dict = {}
    if physicalForm:
        search_dict.update({"物理形态": physicalForm})
    if shape:
        search_dict.update({"形状": shape})
    if pH:
        search_dict.update({"pH": pH})
    # if toc:
    #     search_dict.update({"TOC(%)": toc})
    if cod:
        search_dict.update({"COD(mg/L)": cod})
    if heat:
        search_dict.update({"热值(MJ/kg)": heat})

    # verbosename2name = getData.verbosename2name()
    if physicalNames:
        for k, v in zip(physicalNames, physicalValues):
            if k:
                if v:
                    search_dict.update({k: v})
    if chemicalNames:
        for k, v in zip(chemicalNames, chemicalValues):
            search_dict.update({k: v})

    # for c,k,v in zip(chemicalClass, chemicalNames, chemicalValues):
    #     if c not in search_dict:
    #         search_dict.update({c:[{k:v}]})
    #     else :
    #         search_dict[c].append({k:v})
    # print(search_dict)
    # for item in search_dict:
    #     print(item)

    res = []
    matching_dict = {}
    if search_dict:
        res, matching_dict = Searching5.Matching(search_dict)
    # print(res)
    # idlist = []
    # for i in res[0]:
    #     idlist.append(i+1)

    if res:
        queryset = WasteInfo.objects.filter(固废名称__in=res)
    else:
        queryset = WasteInfo.objects.all()
    
    res_dict = []
    for obj in queryset:
        name = obj.固废名称
        flag = True
        obj_dict = obj.__dict__
        for dict_item in res_dict:
            if dict_item["固废名称"] == name:
                flag = False
                index = res_dict.index(dict_item)
                for item in obj_dict:
                    if (item in useless_label) | (item in text_label):
                        continue
                    else :
                        if obj_dict[item]:
                            if item not in res_dict[index]:
                                res_dict[index][item] = [obj_dict[item]]
                            else:
                                res_dict[index][item].append(obj_dict[item])
                break
        
        if flag:
            res_dict.append({"固废名称": name})
            index = res_dict.index({"固废名称": name})
            # print(res_dict[index][name])
            for item in obj_dict:
                if item in useless_label:
                    continue
                if obj_dict[item]:
                    if item in text_label:
                        res_dict[index][item] = obj_dict[item]
                    else:
                        res_dict[index][item] = [obj_dict[item]]

    if res:
        for item in res_dict:
            item["匹配度"] = matching_dict[item["固废名称"]]
    
    # print(res_dict)        
    # 分页
    page_object = Pagination(request, res_dict, 15)

    # print(queryset)
    # page_object = Pagination(request, queryset, 15)
    models=["匹配度模型","废物产生节点溯源","固相热处理渣类废物溯源","浸出渣类废物溯源","精蒸馏残渣类废物溯源","收尘灰类废物溯源模型1","收尘灰类废物溯源模型2","铝灰溯源判别模型","表面处理污泥溯源判别模型"]
    context = {
        "search_dict": search_dict,
        "physical_solid": physical_solid,
        "physical_halfsolid": physical_halfsolid,
        "physical_liquid": physical_liquid,
        "chemical_solid": chemical_solid,
        "chemical_halfsolid": chemical_halfsolid,
        "chemical_liquid": chemical_liquid,
        "industriolComposition": industriolComposition,
        "elementalComposition": elementalComposition,
        "phaseComposition": phaseComposition,
        "pollutantContent": pollutantContent,
        "PAHs": PAHs,
        "organicPollutant": organicPollutant,
        "toxicLeachingConcentration": toxicLeachingConcentration,
        "pesticide": pesticide,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html(),  # 页码
        "models": models,
    }

    if (search_dict):
        return render(request, 'search_res.html', context)
    return render(request, 'search_label.html', context)




