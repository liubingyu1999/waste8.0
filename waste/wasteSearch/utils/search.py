
import numpy as np
import jieba as jb
import difflib as dl
import copy
import math
from wasteSearch.models import WasteInfo
import re

def DocumentSearch_SingleElement(attributeName, searchText):
    """
    函数名称：DocumentSearch_SingleElement
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于精确的文本搜索。
    适用字段：行业分类、废物类别、物理形态（固态、半固态、液态）、形状（块状、颗粒状、泥状、水状、粘稠状等）
    参数1：attributeName表示字段的名称。
    参数2：searchText表示用户选取的字符串。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    data_original = WasteInfo.objects.values(attributeName)
    data = []
    for i in range(len(data_original)):
        data.append(list(dict.values(data_original[i]))[0])
    result_index = []
    result_matching = []
    # 搜索匹配
    for i in range(len(data)):
        if data[i] == searchText or searchText in data[i]:
            result_index.append(i)
            matching_compatibility = 1.0
            result_matching.append(matching_compatibility)

    return [result_index, result_matching]

def SpeechAnalysis_PositiveAndNegative(text, positiveText, negativeText):
    """
    函数名称：SpeechAnalysis_PositiveAndNegative
    函数功能：对文本进行肯定或否定分析。
    参数1：text表示待分析字符串。
    参数2：positiveText表示表肯定的词库。
    参数3：negativeText表示表否定的词库。
    返回值：描述待分析字符串表示肯定或否定的布尔值。
    """
    textCut = jb.lcut(text)
    value = True
    for i in range(len(textCut)):
        for j in range(len(positiveText)):
            if textCut[i] == positiveText[j]:
                value = True
        for j in range(len(negativeText)):
            if textCut[i] == negativeText[j]:
                value = False

    return value

def DocumentSearch_Binarization(attributeName, searchText):
    """
    函数名称：DocumentSearch_Binarization
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于需要二值化的文本搜索。
    适用字段：磁性
    参数1：attributeName表示字段的名称。
    参数2：searchText表示用户选取的字符串。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    data_original = WasteInfo.objects.values(attributeName)
    data = []
    for i in range(len(data_original)):
        data.append(list(dict.values(data_original[i]))[0])
    data_binary = copy.deepcopy(data)
    for i in range(len(data)):  # 二值化文本数据
        if data[i] == "":
            data_binary[i] = False
        else:
            data_binary[i] = True
    result_index = []
    result_matching = []
    searchValue = SpeechAnalysis_PositiveAndNegative(searchText, positiveWords, negativeWords)
    # 搜索匹配
    for i in range(len(data)):
        if data_binary[i] == searchValue:
            result_index.append(i)
            matching_compatibility = 1.0
            result_matching.append(matching_compatibility)

    return [result_index, result_matching]

def DocumentSearch_BinarizationAndTextAnalysis(attributeName, searchText):
    """
    函数名称：DocumentSearch_BinarizationAndTextAnalysis
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于需要二值化然后进行文本分析的文本搜索。
    适用字段：气味
    参数1：attributeName表示字段的名称。
    参数2：searchText表示用户选取的字符串。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    data_original = WasteInfo.objects.values(attributeName)
    data = []
    for i in range(len(data_original)):
        data.append(list(dict.values(data_original[i]))[0])
    data_binary = copy.deepcopy(data)
    for i in range(len(data)):
        if data[i] == "" or SpeechAnalysis_PositiveAndNegative(data[i], positiveWords, negativeWords) is False:  # 二值化文本数据
            data_binary[i] = False
        else:
            data_binary[i] = True
    result_index = []
    result_matching = []
    searchValue = SpeechAnalysis_PositiveAndNegative(searchText, positiveWords, negativeWords)
    # 搜索匹配
    for i in range(len(data)):
        if data_binary[i] == searchValue:
            if data_binary[i] is False:
                result_index.append(i)
                matching_compatibility = 1.0
                result_matching.append(matching_compatibility)
            else:
                result_index.append(i)
                matching_compatibility = dl.SequenceMatcher(None, searchText, data[i]).ratio()
                result_matching.append(matching_compatibility)

    return [result_index, result_matching]

def DocumentSearch_BinarizationAndMultiElement(attributeName, searchText):
    """
    函数名称：DocumentSearch_MultiElement
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于需要二值化然后精确的多维文本搜索。
    适用字段：表观形貌（球状、板状、粗糙、光滑、团聚、分散）、颜色、物质组成特性、特征指标
    参数1：attributeName表示字段的名称。
    参数2：searchText表示用户选取的字符串列表。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    matching_threshold = 0.5
    # 处理原始数据
    data_original = WasteInfo.objects.values(attributeName)
    data = []
    for i in range(len(data_original)):
        data.append(list(dict.values(data_original[i]))[0])
    data_binary = copy.deepcopy(data)
    for i in range(len(data)):
        if data[i] == "" or SpeechAnalysis_PositiveAndNegative(data[i], positiveWords, negativeWords) is False:  # 二值化文本数据
            data_binary[i] = False
        else:
            data_binary[i] = True
    result_index = []
    result_matching = []
    # 搜索匹配
    dimension = len(searchText)
    if dimension == 1:
        searchValue = SpeechAnalysis_PositiveAndNegative(searchText, positiveWords, negativeWords)
    else:
        searchValue = SpeechAnalysis_PositiveAndNegative(searchText[0], positiveWords, negativeWords)
    for i in range(len(data)):
        matching_compatibility = 0.0
        for j in range(len(searchText)):
            if data_binary[i] == searchValue:
                if data_binary[i] is False:
                    result_index.append(i)
                    matching_compatibility = 1.0
                    result_matching.append(matching_compatibility)
                else:
                    matching_ratio = dl.SequenceMatcher(None, searchText[j], data[i]).quick_ratio()
                    if matching_ratio > matching_threshold or searchText[j] in data[i] or data[i] in searchText[j]:  # 通过正反匹配和阈值的设置判定是否符合
                        matching_compatibility = matching_compatibility+1/dimension

        if matching_compatibility > 0.0:
            result_index.append(i)
            result_matching.append(matching_compatibility)

    return [result_index, result_matching]

def DocumentSearch_SpeechAnalysis(attributeName, searchText):
    """
    函数名称：DocumentSearch_SpeechAnalysis
    函数功能：使用文本描述法在数量有限的范围中模糊搜索符合的数据。
    适用字段：固废名称、产生工段、废物描述、表观形貌（稍微详细）
    参数1：attributeName表示字段的名称。
    参数2：searchText表示用户选取的字符串。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    data_original = WasteInfo.objects.values(attributeName)
    data = []
    for i in range(len(data_original)):
        data.append(list(dict.values(data_original[i]))[0])
    result_index = []
    result_matching = []
    # 搜索匹配
    for i in range(len(data)):
        matching_ratio = dl.SequenceMatcher(None, searchText, data[i]).ratio()
        if matching_ratio > 0.0:
            result_index.append(i)
            matching_compatibility = matching_ratio
            result_matching.append(matching_compatibility)

    return [result_index, result_matching]

def DocumentSearch(attributeName, searchText):
    """
    函数名称：DocumentSearch
    函数功能：使用文本描述法搜索符合的数据。
    参数1：attributeName表示字段的名称。
    参数2：searchText表示用户选取的字符串。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    if attributeName == "行业分类" or attributeName == "废物类别" or attributeName == "物理形态" or \
            attributeName == "形状":
        return DocumentSearch_SingleElement(attributeName, searchText)
    elif attributeName == "磁性":
        return DocumentSearch_Binarization(attributeName, searchText)
    elif attributeName == "气味":
        return DocumentSearch_BinarizationAndTextAnalysis(attributeName, searchText)
    elif attributeName == "颜色" or attributeName == "物质组成特性" or \
            attributeName == "特征指标":
        return DocumentSearch_BinarizationAndMultiElement(attributeName, searchText)
    elif attributeName == "固废名称" or attributeName == "产生工段" or attributeName == "废物描述" or attributeName == "表观形貌稍微详细":
        return DocumentSearch_SpeechAnalysis(attributeName, searchText)

def SimilarityCalculation(x_large, x_small):
    """
    函数名称：SimilarityCalculation
    函数功能：计算两个数值的相似度。
    参数1：x_large表示操作数1。
    参数2：x_small表示操作数2。
    返回值：两个数值的相似度。
    """
    if x_small >= x_large:
        x_small, x_large = x_large, x_small
    x_large = (math.e-1)*x_large
    ratio = x_small/x_large
    similarity = math.e*math.log(ratio+1,math.e)/(ratio+1)
    return similarity

def NumericalSearch(attributeName, searchValue):
    """
    函数名称：NumericalSearch
    函数功能：使用数值描述法在数量有限的范围中模糊搜索符合的数据。
    适用字段：除了使用文本分析的所有字段
    参数1：attributeName表示字段的名称列表。
    参数2：searchValue表示用户选取的数据列表。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    data_original = WasteInfo.objects.values(attributeName)
    data = []
    for i in range(len(data_original)):
        data.append(list(dict.values(data_original[i]))[0])
    for i in range(len(data)):  # 处理原始文本数据
        if(type(data[i]) is str and len(data[i]) > 0):  # 处理带文本的数据
            data[i] = re.sub('[a-zA-Z/]', '', data[i])
            # data[i] = "".join(filter(str.isdigit, data[i]))
            data[i] = float(data[i])
    data_binary = copy.deepcopy(data)
    for i in range(len(data)):
        if data[i] == "":  # 二值化文本数据
            data_binary[i] = False
        else:
            data_binary[i] = True
    result_index = []
    result_matching = []
    # 搜索匹配
    for i in range(len(data)):
        if data_binary[i] is True:
            result_index.append(i)
            matching_compatibility = SimilarityCalculation(float(searchValue), data[i])
            result_matching.append(matching_compatibility)

    return [result_index, result_matching]

def Matching(searchingDict):
    """
    函数名称：Matching
    函数功能：使用文本描述法或数值描述法综合搜索符合的数据。
    参数1：searchingDict表示搜索信息的字典。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    queryset = WasteInfo.objects.filter(dataId__lte=800)
    index_matching = np.arange(len(queryset)).reshape(len(queryset), 1)
    index_matching_add = np.zeros(shape=(len(queryset), 1))
    index_matching = np.c_[index_matching, index_matching_add]
    attributeName = list(dict.keys(searchingDict))
    searchText = list(dict.values(searchingDict))
    document_attribute = ["行业分类", "废物类别", "固废名称", "产生工段", "废物描述", "物理形态",
                          "形状", "表观形貌", "颜色","物质组成特性", "特征指标", "气味", "磁性"]
    result_intersect_index = []

    for i in range(len(attributeName)):
        if attributeName[i] in document_attribute:
            [result_search_index, result_search_matching] = DocumentSearch(attributeName[i], searchText[i])
        else:
            [result_search_index, result_search_matching] = NumericalSearch(attributeName[i], searchText[i])
        for j in range(len(result_search_index)):
            index_matching[result_search_index[j], 1] = index_matching[result_search_index[j], 1]+result_search_matching[j]
        if i == 0:
            result_intersect_index = copy.deepcopy(result_search_index)
        else:
            result_intersect_index = list(set(result_intersect_index) & set(result_search_index))  # 求两个列表的交集

    index_matching = index_matching[result_intersect_index, :]
    index_matching = index_matching[np.argsort(index_matching[:, 1])]
    index_matching = index_matching[::-1, :]

    index = index_matching[:, 0].tolist()
    index = list(map(int, index))
    matching = index_matching[:, 1].tolist()

    return [index, matching]
    # return index_matching


positiveWords = ["有"]
negativeWords = ["没有", "无"]


# index_matching = Matching(all_dict)
# print(index_matching)