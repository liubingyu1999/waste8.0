import pandas as pd
import numpy as np
import jieba as jb
import difflib as dl
import math
from wasteSearch.models import WasteInfo
from wasteSearch import models
from wasteSearch.utils import getData
from django.apps import apps


keyAttribute = "固废名称"
ignoredAttribute = ["废物类别", "行业分类", "固废名称", "别名", "产生工段", "表观形貌(稍微详细)"]
negativeWords = ["没有", "无"]
documentAttribute = ["表观形貌关键词", "物理形态", "形状", "颜色", "气味"]
useless_label= ["_state","id", "序号","dataId"]

# 存储数据库所有数据
res_dict = []
name2index = {}
categoryName = []

gradeAttribute = {"一级指纹": ["表观形貌关键词", "物理形态", "形状", "颜色", "气味", "密度(kg/m3)", "含水率(%)", "pH", "含油率(%)"],
                    "二级指纹": ["COD(mg/L)", "热值(KJ/kg)", "烧失量", "水分", "灰分", "挥发分", "固定碳", "C", "H", "N", "O", "F", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "K", "Ca", "Ti", "V",
                                "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "As", "Pb", "Ag", "Bi", "Cd", "Sn", "Sb", "I", "Hg", "Ba", "Al2O3", "MgO", "P Cl", "K2O", "Na2O",
                                "Fe2O3", "SiO2", "MnO", "CaO", "P S", "SO3", "As2O3", "TiO2", "Cr2O3", "CuO", "ZnO", "PbO", "P F", "V2O5", "BaO", "P2O5", "SnO2", "NiO",
                                "NaCl(%)", "KCl", "MgCl2", "Mg(OH)2", "AlCl3", "MnCl2", "NH4Cl(%)", "TiCl4", "FeCl2", "FeCl3", "CaCl2", "CaF2", "CaSO4", "CaCO3", "P BaO",
                                "BaSO4", "BaCO3", "BaSiO3", "BaS", "NaOH"],
                    "三级指纹": ['辉铜矿', '黄铜矿', '铜铁硫化相', '铁橄榄石', '磁铁矿', '钙铁辉石', '玻璃相', '石膏', '方解石', '石英', '砷铜矿', '皓矾', '六水锌矾', '氧化锑', '三氧化二砷',
                                '五氧化二砷', '铅绿矾', '方铅矿', '铅黄', '铅', '密陀僧', '红锌矿', '闪锌矿', '锌', '纤锌矿', '冰晶石', '刚玉', 'β-氧化铝', '钾冰晶石', '铝', '锥冰晶石',
                                '西蒙冰晶石', '氟铝钙锂石', '白砷石', '三水胆矾', '副雄黄', '砷华', '铅矾', '块黑铅矿', '四水锌矾', '硒汞矿', '尖晶石', '氮化铝', '方镁石', '铜靛矾', 'CuSO4•H2O',
                                'CdSO3•0.5H2O', '石盐', '氟氯铅矿', '铁白云石', '钙铝矾', '氯铅矿','T B', 'T Na', 'T Mg', 'T Al', 'T K', 'T Ca', 'T Fe', 'T Cu', 'T Pb', 'T Zn', 'T Sn', 
                                'T Ni', 'T Co','T Sb', 'T Hg', 'T Cd', 'T Bi', 'T Cr', 'T As', 'T Be', 'T Ba', 'T Pd', 'T Pt', 'T V', 'T Mn', 'T Ti', 'T Al3+','T SO42-', 'CN', 'T F',
                                '萘', '苊烯', '苊', '芴', '菲', '蒽', '荧蒽', '芘', '苯并（a）蒽', '屈', '苯并（b）荧蒽', '苯并 (k)荧蒽', '苯并（a）芘', '茚苯（1,2,3-cd）芘', '二苯并（a, n）蒽', 
                                '苯并（ghi）北（二萘嵌苯）','乙酸乙酯', '乙酸丁酯', '乙酸异戊酯', '氨基甲酸乙酯', '邻甲酸甲酯', '邻甲基苯甲酸', '丁酸丁酯', 'N-氰基乙酰亚胺甲酯（乙酯）', 
                                '4-[3-甲基-3-(（甲亚基氨基)）苯基]丁酸乙酯', '氯甲酸甲酯', '邻苯二甲酸二甲酯', '邻甲基苯甲酸甲酯', '邻苯二甲酸二乙酯','邻苯二甲酸二异丁酯', '邻苯二甲酸二正丁酯', 
                                '邻苯二甲酸二(2-甲氧基)乙酯', '邻苯二甲酸二(4-甲基-2-戊基)酯', '邻苯二甲酸二(2-乙氧基)乙酯', '邻苯二甲酸二戊酯', '邻苯二甲酸二己酯', '邻苯二甲酸丁基苄基酯', 
                                '邻苯二甲酸二(2-丁氧基)乙酯', '邻苯二甲酸二环己酯','邻苯二甲酸二（2-乙基）己酯', '邻苯二甲酸二苯酯', '邻苯二甲酸二正辛酯', '邻苯二甲酸二壬酯', '苯', '甲苯', '乙苯', 
                                '二甲苯', '对二甲苯', '间二甲苯', '邻二甲苯', '异丙苯', '苯乙烯', '乙烯基甲苯', '环己烷', '二氯甲烷', '二氯乙烷', '苯酚', '邻甲酚','2,4-二氯酚', '2,5-二氯苯酚', 
                                '甲醛', '间苯氧基苯甲醛', '甲酸', '苯氧乙酸', '氯乙酸', '羟基乙酸', '2甲4氯酸', '甘氨酸', '亚磷酸钠', '甲基草甘膦酸钠盐', '羟甲基磷酸钠盐', '2,4-二氯苯氧乙酸钠',
                                '氯甲基吡啶', '吡啶', '2-氯-5-氯甲基吡啶', '三氯吡啶醇钠', '乙基氯化物', '氯乙酰氯', '邻苯二胺', '苯肼', '脲', '1-苯基氨基脲', '二甲胺', '2-氯烟酰胺', '精胺', 
                                '胺醚', '乙撑硫脲', '邻甲基苯基硫脲', '2-氯-N-(氯甲基)-N-(2,6-二乙基苯基)乙酰胺（MRM）','N-2,6-二乙基苯基甲亚胺（甲叉）', '丁草胺', '4-[3-乙基-2-(甲亚基氨基)苯基]丁酰氯', 
                                '2,5-二氯苯胺','2,4-D', '草甘膦', '增甘膦', '双甘膦', '西玛津', '三唑磷', '烟嘧磺酰氯', '烟嘧磺胺', '烟嘧磺隆(mg/kg)','毒死蜱', '多菌灵', '氟乐灵', '丁草胺', 
                                '咪鲜胺', '莠去津', '百草枯', '苯磺隆', '吡虫啉', '咪唑（烷）', '丙环唑', '代森锰', '敌百虫', '啶虫脒', '麦草畏', '杀虫单', '乙草胺', '溴丙烷', '四氯化碳', '丙溴磷', 
                                '对氯三氟甲苯','功夫酰氯', '苄基三乙基氯化铵','二氯菊酰氯', '4-甲基-2-肼基苯并骈噻唑', '苯唑醇', '二甲硫醚', '硫酸二甲酯', '甲醇', '乙醇', '辛硫磷', 
                                'O,O-二乙基硫代磷酰氯','醋酸', '醋酸酐', '丙烯醛', '丙烯腈', '环戊二烯','L Ca', 'L Mg', 'L Fe', 'L Cu', 'L Pb', 'L Zn', 'L Ba', 'L Sn', 'L Co', 'L Sb', 
                                'L Hg', 'L Cd', 'L Bi', 'L Ni', 'L Cr', 'L Ag', 'L As','L Se', 'L Br', 'L V', 'L F']}

def get_value(attribute_name, category_name):
    """
    函数名称：get_value
    函数功能：获取数据里的数据。
    参数1：attribute_name表示字段的名称。
    参数2：category_name表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    allValue = []
    
    datarecord = res_dict[name2index[category_name]]
    value = ''
    if attribute_name in documentAttribute:
        if attribute_name in datarecord:
            for item in datarecord[attribute_name]:
                if item not in allValue:
                    allValue.append(item)
                    value = value + item + ';'
        value = value[:-1]
    else:
        if attribute_name in datarecord:
            for item in datarecord[attribute_name]:
                if (item != None) and (item != 'ND') and (item != ' '):
                    if '-' in item:
                        s, l = item.split('-', 1)
                        allValue.append(float(s))
                        allValue.append(float(l))
                    elif (item[0] == '≤') or (item[0] =='<'):
                        allValue.append(float(item[1]))
                    else:
                        allValue.append(float(item))
        if len(allValue):
            upper = max(allValue)
            lower = min(allValue)
            if upper == lower :
                value = str(upper)
            else:
                value = str(lower) + '~' + str(upper)
    # queryset = models.WasteInfo.objects.filter(固废名称=category_name).all()
    # verboseName2name = getData.verbosename2name()
    # modelName = verboseName2name[attribute_name]
    # 
    # if attribute_name in documentAttribute:
    #     for obj in queryset:
    #         obj_dict = obj.__dict__
    #         if (obj_dict[modelName] != None) and (obj_dict[modelName] != 'ND') and (obj_dict[modelName] != ' '):
    #             if obj_dict[modelName] not in allValue:
    #                 allValue.append(obj_dict[modelName])
    #                 value = value + obj_dict[modelName] + ';'
    #     value = value[:-1]
    # else:
    #     for obj in queryset:
    #         obj_dict = obj.__dict__
    #         if (obj_dict[modelName] != None) and (obj_dict[modelName] != 'ND') and (obj_dict[modelName] != ' '):
    #             if '-' in obj_dict[modelName]:
    #                 s, l = range.split('-', 1)
    #                 allValue.append(float(s))
    #                 allValue.append(float(l))
    #             elif (obj_dict[modelName][0] == '≤') or (obj_dict[modelName][0] =='<'):
    #                 allValue.append(float(obj_dict[modelName][1]))
    #             else:
    #                 allValue.append(float(obj_dict[modelName]))
    #     if len(allValue):
    #         upper = max(allValue)
    #         lower = min(allValue)
    #         if upper == lower :
    #             value = str(upper)
    #         else:
    #             value = str(lower) + '~' + str(upper)

    if value:
        return value
    else:
        return str(-1)


def document_search_single_element(attribute_name, search_text, category_name):
    """
    函数名称：document_search_single_element
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于精确的文本搜索。
    适用字段：物理形态、形状
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：category_name表示废物的名称。
    返回值：样本的匹配度。
    """
    # 处理原始数据
    data = get_value(attribute_name, category_name)
    if data == -1:
        return 0.0
    if ";" in data:
        str_list = []
        substr_begin = 0
        for i in range(len(data)):
            if data[i] == ";" and i != len(data) - 1:
                str_list.append(data[substr_begin:i])
                substr_begin = i + 1
            if i == len(data) - 1:
                str_list.append(data[substr_begin:])
        data = str_list
    result_matching = 0.0
    # 搜索匹配
    if type(data) == str:
        if search_text == data:
            result_matching = 1.0
    elif type(data) == list:
        if search_text in data:
            result_matching = 1.0

    return result_matching


def speech_analysis_positive_negative(text, negative_text):
    """
    函数名称：speech_analysis_positive_negative
    函数功能：对文本进行肯定或否定分析。
    参数1：text表示待分析字符串。
    参数2：negative_text表示表否定的词库。
    返回值：描述待分析字符串表示肯定或否定的布尔值。
    """
    textCut = jb.lcut(text)
    value = True
    for i in range(len(textCut)):
        for j in range(len(negative_text)):
            if textCut[i] == negative_text[j]:
                value = False

    return value


def document_search_binarization_text_analysis(attribute_name, search_text, category_name):
    """
    函数名称：document_search_binarization_textanalysis
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于需要二值化然后进行文本分析的文本搜索。
    适用字段：气味
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：category_name表示废物的名称。
    返回值：样本的匹配度。
    """
    # 处理原始数据
    data = get_value(attribute_name, category_name)
    if data == -1:
        return 0.0
    if ";" in data:
        str_list = []
        substr_begin = 0
        for i in range(len(data)):
            if data[i] == ";" and i != len(data) - 1:
                str_list.append(data[substr_begin:i])
                substr_begin = i + 1
            if i == len(data) - 1:
                str_list.append(data[substr_begin:])
        data = str_list
    result_matching = 0.0
    # 二值化文本数据
    data_binary = False
    if type(data) == list:
        data_binary = True
    elif type(data) == str:
        if data == "" or speech_analysis_positive_negative(data, negativeWords) is False:  # 二值化文本数据
            data_binary = False
        else:
            data_binary = True
    search_value = speech_analysis_positive_negative(search_text, negativeWords)
    # 搜索匹配
    if data_binary == search_value:
        if type(data) == list:
            result_matching = 0.1  # 一个较小的默认匹配值
            for i in range(len(data)):
                matching_compatibility_temp = dl.SequenceMatcher(None, search_text, data[i]).ratio()
                if matching_compatibility_temp > result_matching:
                    result_matching = matching_compatibility_temp
        elif type(data) == str:
            if data_binary is False:
                result_matching = 1.0
            else:
                result_matching = dl.SequenceMatcher(None, search_text, data).ratio()

    return result_matching


def document_search_binarization_multi_element(attribute_name, search_text, category_name):
    """
    函数名称：document_search_binarization_multi_element
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于需要二值化然后精确的多维文本搜索。
    适用字段：表观形貌、颜色
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：category_name表示废物的名称。
    返回值：样本的匹配度。
    """
    # 处理原始数据
    data = get_value(attribute_name, category_name)
    if data == -1:
        return 0.0
    if ";" in data:
        str_list = []
        substr_begin = 0
        for i in range(len(data)):
            if data[i] == ";" and i != len(data) - 1:
                str_list.append(data[substr_begin:i])
                substr_begin = i + 1
            if i == len(data) - 1:
                str_list.append(data[substr_begin:])
        data = str_list
    result_matching = 0.0
    # 二值化文本数据
    data_binary = False
    if type(data) == list:
        data_binary = True
    elif type(data) == str:
        if data == "" or speech_analysis_positive_negative(data, negativeWords) is False:  # 二值化文本数据
            data_binary = False
        else:
            data_binary = True
    search_value = speech_analysis_positive_negative(search_text, negativeWords)
    # 搜索匹配
    search_text_cut = jb.lcut(search_text)
    i = 0
    if search_value is True:
        while i < len(search_text_cut):  # 处理符号
            if search_text_cut[i] == "。" or search_text_cut[i] == "，" or search_text_cut[i] == "：" or search_text_cut[i] == "、" or \
                    search_text_cut[i] == "/" or search_text_cut[i] == "（" or search_text_cut[i] == "）" or search_text_cut[i] == "无" or \
                    search_text_cut[i] == "等":
                search_text_cut.remove(search_text_cut[i])
                i = i - 1
            if "色" in search_text_cut[i]:
                search_text_cut[i] = search_text_cut[i].replace("色", "")
            i = i + 1
    if data_binary == search_value:
        if type(data) == list:
            matching_compatibility = 0.0
            for i in range(len(data)):
                data_temp = jb.lcut(data[i])
                j = 0
                while j < len(data_temp):  # 处理符号
                    if data_temp[j] == "。" or data_temp[j] == "，" or data_temp[j] == "：" or data_temp[j] == "、" or data_temp[j] == "/" or \
                            data_temp[j] == "（" or data_temp[j] == "）" or data_temp[j] == "无" or data_temp[j] == "等":
                        data_temp.remove(data_temp[j])
                        j = j - 1
                    j = j + 1
                dimension = len(data_temp)
                matching_compatibility_temp = 0.0
                for j in range(len(data_temp)):
                    for k in range(len(search_text_cut)):
                        if data_temp[j] in search_text_cut[k] or search_text_cut[k] in data_temp[j]:
                            matching_compatibility_temp = matching_compatibility_temp + 1 / dimension
                if matching_compatibility_temp > matching_compatibility:
                    matching_compatibility = matching_compatibility_temp
            if matching_compatibility > 0.0:
                result_matching = matching_compatibility
        elif type(data) == str:
            if data_binary is False:
                result_matching = 1.0
            else:
                data_temp = jb.lcut(data)
                i = 0
                while i < len(data_temp):  # 处理符号
                    if data_temp[i] == "。" or data_temp[i] == "，" or data_temp[i] == "：" or data_temp[i] == "、" or data_temp[i] == "/" or \
                            data_temp[i] == "（" or data_temp[i] == "）" or data_temp[i] == "无" or data_temp[i] == "等":
                        data_temp.remove(data_temp[i])
                        i = i - 1
                    i = i + 1
                dimension = len(data_temp)
                matching_compatibility = 0.0
                for j in range(len(data_temp)):
                    for k in range(len(search_text_cut)):
                        if data_temp[j] in search_text_cut[k] or search_text_cut[k] in data_temp[j]:
                            matching_compatibility = matching_compatibility + 1 / dimension
                if matching_compatibility > 0.0:
                    result_matching = matching_compatibility

    return result_matching


def document_search(attribute_name, search_text, category_name):
    """
    函数名称：document_search
    函数功能：使用文本描述法搜索符合的数据。
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：category_name表示废物的名称。
    返回值：样本的匹配度。
    """
    if attribute_name == "物理形态" or attribute_name == "形状":
        return document_search_single_element(attribute_name, search_text, category_name)
    elif attribute_name == "气味":
        return document_search_binarization_text_analysis(attribute_name, search_text, category_name)
    elif attribute_name == "表观形貌关键词" or attribute_name == "颜色":
        return document_search_binarization_multi_element(attribute_name, search_text, category_name)


def similarity_calculation(x_large, x_small):
    """
    函数名称：similarity_calculation
    函数功能：计算两个数值的相似度。
    参数1：x_large表示操作数1。
    参数2：x_small表示操作数2。
    返回值：两个数值的相似度。
    """
    if x_small >= x_large:
        x_small, x_large = x_large, x_small
    x_large = (math.e - 1) * x_large
    ratio = x_small / x_large
    similarity = math.e * math.log(ratio + 1, math.e) / (ratio + 1)
    return similarity


def numerical_search_absolute_value(attribute_name, search_value, category_name):
    """
    函数名称：numerical_search_absolute_value
    函数功能：使用数值描述法在数量有限的范围中模糊搜索符合的数据。
    适用字段：以绝对值为单位的数值型数据对应的字段。
    参数1：attribute_name表示字段的名称列表。
    参数2：search_value表示用户选取的数据列表。
    参数3：category_name表示废物的名称。
    返回值：样本的匹配度。
    """
    # 处理原始数据
    data = get_value(attribute_name, category_name)
    if data == -1:
        return 0.0
    data_min = 0.0
    data_max = 0.0
    if "~" in data:
        substr_begin = 0
        for i in range(len(data)):
            if data[i] == "~" and i != len(data) - 1:
                data_min = float(data[substr_begin:i])
                substr_begin = i + 1
            if i == len(data) - 1:
                data_max = float(data[substr_begin:])
    else:
        data_min = float(data)
        data_max = float(data)
    result_matching = 0.0
    search_value = float(search_value)
    # 搜索匹配
    if data_min != data_max:
        if data_min <= search_value <= data_max:
            result_matching = 1.0
        elif search_value < data_min:
            result_matching = similarity_calculation(float(search_value), data_min)
        elif search_value > data_max:
            result_matching = similarity_calculation(data_max, float(search_value))
    elif data_min == data_max:
        result_matching = similarity_calculation(data_min, float(search_value))

    return result_matching


def numerical_search_percentage_value(attribute_name, search_value, category_name):
    """
    函数名称：numerical_search_percentage_value
    函数功能：使用数值描述法在数量有限的范围中模糊搜索符合的数据。
    适用字段：以百分比为单位的数值型数据对应的字段。
    参数1：attribute_name表示字段的名称列表。
    参数2：search_value表示用户选取的数据列表。
    参数3：category_name表示废物的名称。
    返回值：样本的匹配度。
    """
    # 处理原始数据
    data = get_value(attribute_name, category_name)
    if data == -1:
        return 0.0
    data_min = 0.0
    data_max = 0.0
    if "~" in data:
        substr_begin = 0
        for i in range(len(data)):
            if data[i] == "~" and i != len(data) - 1:
                data_min = float(data[substr_begin:i])
                substr_begin = i + 1
            if i == len(data) - 1:
                data_max = float(data[substr_begin:])
    else:
        data_min = float(data)
        data_max = float(data)
    result_matching = 0.0
    # 搜索匹配
    search_value = float(search_value)
    if data_min != data_max:
        if data_min <= search_value <= data_max:
            result_matching = 1.0
    elif data_min == data_max:
        if search_value < data_min:
            if search_value > data_min * 0.8:
                result_matching = similarity_calculation(float(search_value), data_min)
        elif search_value == data_min:
            result_matching = 1.0
        elif search_value > data_max:
            if search_value < data_max * 1.2:
                result_matching = similarity_calculation(data_max, float(search_value))

    return result_matching


def numerical_search(attribute_name, search_value, category_name):
    """
    函数名称：numerical_search
    函数功能：使用数值描述法搜索符合的数据。
    参数1：attribute_name表示字段的名称。
    参数2：search_value表示用户选取的数据列表。
    参数3：category_name表示废物的名称。
    返回值：样本的匹配度。
    """
    absolute_value_attribute = ["密度(kg/m3)", "pH", "COD(mg/L)", "热值(KJ/kg)", "T B", "T Na", "T Mg", "T Al", "T K", "T Ca", "T Fe", "T Cu", "T Pb", "T Zn", "T Sn", "T Ni", "T Co", "T Sb", "T Hg",
                                "T Cd", "T Bi", "T Cr", "T As", "T Be", "T Ba", "T Pd", "T Pt", "T V", "T Mn", "T Ti", "T Al3+ ", "T SO42- ", "CN", "T F", "萘", "苊烯", "苊", "芴",
                                "菲", "蒽", "荧蒽", "芘", "苯并（a）蒽", "屈", "苯并（b）荧蒽", "苯并 (k)荧蒽", "苯并（a）芘", "茚苯（1,2,3-cd）芘", " 二苯并（a, n）蒽",
                                "苯并（ghi）北（二萘嵌苯）", "乙酸乙酯", "乙酸丁酯", "乙酸异戊酯", "氨基甲酸乙酯", "邻甲酸甲酯", "邻甲基苯甲酸", "丁酸丁酯", "N-氰基乙酰亚胺甲酯（乙酯）",
                                "4-[3-甲基-3-(（甲亚基氨基)）苯基]丁酸乙酯", "氯甲酸甲酯", "邻苯二甲酸二甲酯", "邻甲基苯甲酸甲酯", "邻苯二甲酸二乙酯", "邻苯二甲酸二异丁酯",
                                "邻苯二甲酸二正丁酯", "邻苯二甲酸二(2-甲氧基)乙酯", "邻苯二甲酸二(4-甲基-2-戊基)酯", "邻苯二甲酸二(2-乙氧基)乙酯", "邻苯二甲酸二戊酯", "邻苯二甲酸二己酯",
                                "邻苯二甲酸丁基苄基酯", "邻苯二甲酸二(2-丁氧基)乙酯", "邻苯二甲酸二环己酯", "邻苯二甲酸二（2-乙基）己酯", "邻苯二甲酸二苯酯", "邻苯二甲酸二正辛酯",
                                "邻苯二甲酸二壬酯", "苯", "甲苯", "乙苯", "二甲苯", "对二甲苯", "间二甲苯", "邻二甲苯", "异丙苯", "苯乙烯", "乙烯基甲苯", "环己烷", "二氯甲烷", "二氯乙烷",
                                "苯酚", "邻甲酚", "2,4-二氯酚", "2,5-二氯苯酚", "甲醛", "间苯氧基苯甲醛", "甲酸", "苯氧乙酸", "氯乙酸", "羟基乙酸", "2甲4氯酸", "甘氨酸", "亚磷酸钠",
                                "甲基草甘膦酸钠盐", "羟甲基磷酸钠盐", "2,4-二氯苯氧乙酸钠", "氯甲基吡啶", "吡啶", "2-氯-5-氯甲基吡啶", "三氯吡啶醇钠", "乙基氯化物", "氯乙酰氯", "邻苯二胺",
                                "苯肼", "脲", "1-苯基氨基脲", "二甲胺", "2-氯烟酰胺", "精胺", "胺醚", "乙撑硫脲", "邻甲基苯基硫脲", "2-氯-N-(氯甲基)-N-(2,6-二乙基苯基)乙酰胺（MRM）",
                                "N-2,6-二乙基苯基甲亚胺（甲叉）", "丁草胺", "4-[3-乙基-2-(甲亚基氨基)苯基]丁酰氯", "2,5-二氯苯胺", "2,4-D", "草甘膦", "增甘膦",
                                "双甘膦", "西玛津", "三唑磷", "烟嘧磺酰氯", "烟嘧磺胺", "烟嘧磺隆(mg/kg)", "毒死蜱", "多菌灵", "氟乐灵", "咪鲜胺", "莠去津mg/L",
                                "百草枯", "苯磺隆", "吡虫啉", "咪唑（烷）", "丙环唑", "代森锰mg/L", "敌百虫", "啶虫脒", "麦草畏", "杀虫单", "乙草胺", "溴丙烷", "四氯化碳",
                                "丙溴磷", "对氯三氟甲苯", "功夫酰氯", "苄基三乙基氯化铵", "二氯菊酰氯", "4-甲基-2-肼基苯并骈噻唑", "苯唑醇", "二甲硫醚", "硫酸二甲酯", "甲醇", "乙醇",
                                "辛硫磷", "O,O-二乙基硫代磷酰氯", "醋酸", "醋酸酐", "丙烯醛", "丙烯腈", "环戊二烯", "L Ca", "L Mg", "L Fe", "L Cu", "L Pb", "L Zn", "L Ba", "L Sn ",
                                "L Co", "L Sb", "L Hg", "L Cd", "L Bi", "L Ni", "L Cr ", "L Ag", "L As", "L Se", "L Br", "L V", "L F"]
    percentage_attribute = ["含水率(%)", "含油率(%)", "烧失量", "水分", "灰分", "挥发分", "固定碳", "C", "H", "N", "O", "F", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "K", "Ca", "Ti", "V",
                            "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "As", "Pb", "Ag", "Bi", "Cd", "Sn", "Sb", "I", "Hg", "Ba", "Al2O3", "MgO", "P Cl", "K2O", "Na2O", "Fe2O3",
                            "SiO2", "MnO", "CaO", "P S", "SO3", "As2O3", "TiO2", "Cr2O3", "CuO", "ZnO", "PbO", "P F", "V2O5", "BaO", "P2O5", "SnO2", "NiO", "NaCl(%)", "KCl",
                            "MgCl2", "Mg(OH)2", "AlCl3", "MnCl2", "NH4Cl(%)", "TiCl4", "FeCl2", "FeCl3", "CaCl2", "CaF2", "CaSO4", "CaCO3", "P BaO", "BaSO4", "BaCO3", "BaSiO3",
                            "BaS", "NaOH", "辉铜矿", "黄铜矿", "铜铁硫化相", "铁橄榄石", "磁铁矿", "钙铁辉石", "玻璃相", "石膏", "方解石", "石英", "砷铜矿", "皓矾", "六水锌矾", "氧化锑",
                            "三氧化二砷", "五氧化二砷", "铅绿矾", "方铅矿", "铅黄", "铅", "密陀僧", "红锌矿", "闪锌矿", "锌", "纤锌矿", "冰晶石", "刚玉", "β-氧化铝", "钾冰晶石", "铝",
                            "锥冰晶石", "西蒙冰晶石", "氟铝钙锂石", "白砷石", "三水胆矾", "副雄黄", "砷华", "铅矾", "块黑铅矿", "四水锌矾", "硒汞矿", "尖晶石", "氮化铝", "方镁石",
                            "铜靛矾", "CuSO4•H2O", "CdSO3•0.5H2O", "石盐", "氟氯铅矿", "铁白云石", "钙铝矾", "氯铅矿"]
        
    if attribute_name in absolute_value_attribute:
        return numerical_search_absolute_value(attribute_name, search_value, category_name)
    elif attribute_name in percentage_attribute:
        return numerical_search_percentage_value(attribute_name, search_value, category_name)



def matching_data(searching_dict, weight):
    """
    函数名称：match_matching_data
    函数功能：使用文本描述法或数值描述法综合搜索符合的数据。
    参数1：searching_dict表示搜索信息的字典。
    参数2：weight表示每项数据的权重。
    返回值：样本的名称列表、样本的匹配度列表。
    """
    matching_name = np.array(categoryName).reshape(len(categoryName), 1)
    matching_add = np.zeros(shape=(len(categoryName), 1))
    matching = np.c_[matching_name, matching_add]
    attribute_name = list(searching_dict.keys())
    search_text = list(searching_dict.values())

    for i in range(matching.shape[0]):
        error_num = 0
        for j in range(len(attribute_name)):
            if attribute_name[j] in documentAttribute:
                result_search_matching = document_search(attribute_name[j], search_text[j], categoryName[i])
            else:
                result_search_matching = numerical_search(attribute_name[j], search_text[j], categoryName[i])
            if result_search_matching > 0:
                if attribute_name[j] in gradeAttribute["一级指纹"]:
                    result_search_matching = result_search_matching * weight[0]
                elif attribute_name[j] in gradeAttribute["二级指纹"]:
                    result_search_matching = result_search_matching * weight[1]
                elif attribute_name[j] in gradeAttribute["三级指纹"]:
                    result_search_matching = result_search_matching * weight[2]
            else:
                error_num = error_num + 1
            if error_num <= 3:
                matching[i, 1] = float(matching[i, 1]) + result_search_matching
            else:
                matching[i, 1] = 0.0
                break

    index_matching = matching[np.argsort(matching[:, 1])]
    index_matching = index_matching[::-1, :]
    zero_result = []
    for i in range(index_matching.shape[0]):
        if index_matching[i, 1] == 0:
            zero_result.append(i)
    index_matching = np.delete(index_matching, zero_result, axis=0)
    result_name = index_matching[:, 0].tolist()
    result_matching = index_matching[:, 1].tolist()
    if len(result_name) > 5:
        result_name = result_name[0:5]
        result_matching = result_matching[0:5]

    return result_name, result_matching

def getalldata():
    name2verboseName = {}
    fields = apps.get_model('wasteSearch.WasteInfo')._meta.fields
    # 建立models中存储的表名还原
    for item in fields:
        name2verboseName[item.name] = item.verbose_name

    queryset = WasteInfo.objects.all()
    for obj in queryset:
        name = obj.固废名称
        flag = True
        obj_dict = obj.__dict__
        for dict_item in res_dict:
            if dict_item["固废名称"] == name:
                flag = False
                index = res_dict.index(dict_item)
                for item in obj_dict:
                    if (item in useless_label) | (item in ignoredAttribute):
                        continue
                    else :
                        if obj_dict[item]:
                            verbosename = name2verboseName[item]
                            if verbosename not in res_dict[index]:
                                res_dict[index][verbosename] = [obj_dict[item]]
                            else:
                                res_dict[index][verbosename].append(obj_dict[item])
                break
        
        if flag:
            res_dict.append({"固废名称": name})
            index = res_dict.index({"固废名称": name})
            # print(res_dict[index][name])
            for item in obj_dict:
                if item in useless_label:
                    continue
                verbosename = name2verboseName[item]
                if obj_dict[item]:
                    if item in ignoredAttribute:
                        res_dict[index][verbosename] = obj_dict[item]
                    else:
                        res_dict[index][verbosename] = [obj_dict[item]]
    i = 0
    for item in res_dict:
        name2index[item['固废名称']] = i
        i += 1

def Matching(search_dict):
    for item in models.WasteInfo.objects.all():
        n = item.固废名称
        if n != None:
            if n not in categoryName:
                categoryName.append(n)
    # 文本识别
    attributeWeight = [1, 1, 1]
    # print(search_dict)
    # allDict = {"物理形态": "半固态", "表观形貌关键词": "板状、光滑、团聚", "含水率": 48.8, "形状": "泥状", "Al2O3": 0.41}
    getalldata()

    resultName, resultMatching = matching_data(search_dict, attributeWeight)
    resultDict = {}
    search_len = len(search_dict)
    for i in range(0, len(resultName)):
        accuracy = (float(resultMatching[i])/search_len) * 100
        accuracy = round(accuracy,2)
        resultDict[resultName[i]] = str(accuracy)+"%"
    # print(resultDict)
    return resultName,resultDict

