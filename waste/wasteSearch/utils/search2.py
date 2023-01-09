import pandas as pd
import numpy as np
import jieba as jb
import difflib as dl
import copy
import math
from wasteSearch.models import WasteInfo


def document_search_single_element(attribute_name, search_text, row_index):
    """
    函数名称：document_search_single_element
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于精确的文本搜索。
    适用字段：行业分类、废物类别、物理形态(固态、半固态、液态)、形状(块状、颗粒状、泥状、水状、粘稠状等)
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：row_index表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    columns_name = sortedData.columns.tolist()
    columns_index = []
    for i in range(len(columns_name)):
        if attribute_name == columns_name[i]:
            columns_index.append(i)
            break
    data = sortedData.iloc[row_index, columns_index].tolist()
    data = data[0]
    if data != data:  # nan类型的数据与自己不相等
        data = ""
    elif ";" in data:
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
    if search_text == data:
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


def document_search_binarization(attribute_name, search_text, row_index):
    """
    函数名称：document_search_binarization
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于需要二值化的文本搜索。
    适用字段：磁性
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：row_index表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    columns_name = sortedData.columns.tolist()
    columns_index = []
    for i in range(len(columns_name)):
        if attribute_name == columns_name[i]:
            columns_index.append(i)
            break
    data = sortedData.iloc[row_index, columns_index].tolist()
    data = data[0]
    if data != data:  # nan类型的数据与自己不相等
        data = ""
    elif ";" in data:
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
    for i in range(len(data)):
        if data != "":
            data_binary = True
    search_value = speech_analysis_positive_negative(search_text, negativeWords)
    # 搜索匹配
    if data_binary == search_value:
        result_matching = 1.0

    return result_matching


def document_search_binarization_text_analysis(attribute_name, search_text, row_index):
    """
    函数名称：document_search_binarization_textanalysis
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于需要二值化然后进行文本分析的文本搜索。
    适用字段：气味
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：row_index表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    columns_name = sortedData.columns.tolist()
    columns_index = []
    for i in range(len(columns_name)):
        if attribute_name == columns_name[i]:
            columns_index.append(i)
            break
    data = sortedData.iloc[row_index, columns_index].tolist()
    data = data[0]
    if data != data:  # nan类型的数据与自己不相等
        data = ""
    elif ";" in data:
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


def document_search_binarization_multi_element(attribute_name, search_text, row_index):
    """
    函数名称：document_search_binarization_multi_element
    函数功能：使用文本描述法在数量有限的范围中精确搜索符合的数据，它适用于需要二值化然后精确的多维文本搜索。
    适用字段：表观形貌(球状、板状、粗糙、光滑、团聚、分散)、颜色、物质组成特性
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：row_index表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    columns_name = sortedData.columns.tolist()
    columns_index = []
    for i in range(len(columns_name)):
        if attribute_name == columns_name[i]:
            columns_index.append(i)
            break
    data = sortedData.iloc[row_index, columns_index].tolist()
    data = data[0]
    if data != data:  # nan类型的数据与自己不相等
        data = ""
    elif ";" in data:
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


def document_search(attribute_name, search_text, row_index):
    """
    函数名称：document_search
    函数功能：使用文本描述法搜索符合的数据。
    参数1：attribute_name表示字段的名称。
    参数2：search_text表示用户选取的字符串。
    参数3：row_index表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    if attribute_name == "废物类别" or attribute_name == "行业分类" or attribute_name == "物理形态(固态、半固态、液态)" or \
            attribute_name == "形状(块状、颗粒状、泥状、水状、粘稠状等)":
        return document_search_single_element(attribute_name, search_text, row_index)
    elif attribute_name == "磁性":
        return document_search_binarization(attribute_name, search_text, row_index)
    elif attribute_name == "气味":
        return document_search_binarization_text_analysis(attribute_name, search_text, row_index)
    elif attribute_name == "表观形貌(球状、板状、粗糙、光滑、团聚、分散)" or attribute_name == "颜色" or attribute_name == "物质组成特性":
        return document_search_binarization_multi_element(attribute_name, search_text, row_index)


def numerical_search_absolute_value(attribute_name, search_value, row_index):
    """
    函数名称：numerical_search_absolute_value
    函数功能：使用数值描述法在数量有限的范围中模糊搜索符合的数据。
    适用字段：以绝对值为单位的数值型数据对应的字段。
    参数1：attribute_name表示字段的名称列表。
    参数2：search_value表示用户选取的数据列表。
    参数3：row_index表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    columns_name = sortedData.columns.tolist()
    columns_index = []
    for i in range(len(columns_name)):
        if attribute_name == columns_name[i]:
            columns_index.append(i)
            break
    data = sortedData.iloc[row_index, columns_index].tolist()
    data = data[0]
    data_min = 0.0
    data_max = 0.0
    if data != data:  # nan类型的数据与自己不相等
        data = ""
    else:
        if type(data) is float:
            data_min = data
            data_max = data
        elif type(data) is str:
            for i in range(len(data)):
                if data[i] == "~":
                    data_min = float(data[:i])
                    data_max = float(data[i + 1:])
                    break
    result_matching = 0.0
    # 二值化文本数据
    if data != "":
        data_binary = True
    else:
        data_binary = False
    # 搜索匹配
    if data_binary is True:
        if data_min <= float(search_value) <= data_max:
            result_matching = 1.0

    return result_matching


def numerical_search_binarization(attribute_name, row_index):
    """
    函数名称：numerical_search_binarization
    函数功能：使用数值描述法在数量有限的范围中模糊搜索符合的数据。
    适用字段：使用二值化处理的数值型数据对应的字段。
    参数1：attribute_name表示字段的名称列表。
    参数2：row_index表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    # 处理原始数据
    columns_name = sortedData.columns.tolist()
    columns_index = []
    for i in range(len(columns_name)):
        if attribute_name == columns_name[i]:
            columns_index.append(i)
            break
    data = sortedData.iloc[row_index, columns_index].tolist()
    data = data[0]
    # 二值化文本数据
    if data != data:  # nan类型的数据与自己不相等
        data_binary = False
    else:
        data_binary = True
    result_matching = 0.0
    # 搜索匹配
    if data_binary is True:
        result_matching = 1.0

    return result_matching


def numerical_search(attribute_name, search_value, row_index):
    """
    函数名称：numerical_search
    函数功能：使用数值描述法搜索符合的数据。
    参数1：attribute_name表示字段的名称。
    参数2：search_value表示用户选取的数据列表。
    参数3：row_index表示废物的名称。
    返回值：样本的索引列表、样本的匹配度列表。
    """
    absolute_value_attribute = numericalAttribute["绝对数值"]
    binarization_attribute = numericalAttribute["二值化数值"]
    if attribute_name in absolute_value_attribute:
        return numerical_search_absolute_value(attribute_name, search_value, row_index)
    elif attribute_name in binarization_attribute:
        return numerical_search_binarization(attribute_name, row_index)


def process_extracting_data(data, key_column, ignored_column, column_range):
    """
    函数名称：process_extracting_data
    函数功能：提取数据库中的信息。
    参数1：data表示原始数据库。
    参数2：key_column表示原始数据库的主键。
    参数3：ignored_column表示原始数据库中可以忽略字段名称的列表。
    参数4：column_range表示原始数据库中字段类型的字典。
    返回值1：numerical_attribute_column表示数值型数据对应字段所在的列的字典。
    返回值2：numerical_attribute_type表示数值型数据对应父字段包含内容的字典。
    """
    ignored_column.append(key_column)
    new_data = pd.DataFrame(data)
    columns_name = new_data.iloc[0, :].tolist()
    # 获取数值型字段的名称
    numerical_attribute_column = {}
    numerical_attribute_type = {}
    for key_field_name in column_range.keys():
        key_index_first = columns_name.index(column_range[key_field_name][0])
        key_index_last = columns_name.index(column_range[key_field_name][1]) + 1
        numerical_attribute_column[key_field_name] = [key_index_first, key_index_last]
        numerical_attribute_type[key_field_name] = columns_name[key_index_first:key_index_last]

    return [numerical_attribute_column, numerical_attribute_type]


def process_processing_data(data, key_column, ignored_column, numerical_attribute_column, numerical_attribute_type):
    """
    函数名称：processing_data
    函数功能：处理数据库中的信息。
    参数1：data表示原始数据库。
    参数2：key_column表示原始数据库的主键。
    参数3：ignored_column表示原始数据库中可以忽略字段名称的列表。
    参数4：numerical_attribute_column表示数值型数据对应字段所在的列的字典。
    参数5：numerical_attribute_type表示数值型数据对应父字段包含内容的字典。
    返回值：frame_data表示根据主键筛选的数据库。
    """
    ignored_column.append(key_column)
    process_data = pd.DataFrame(data)
    columns_name = process_data.iloc[0, :].tolist()
    # 修改表格的字段名
    process_data.columns = columns_name
    process_data.drop(index=[0], inplace=True)  # 删除原数据的第一行数据
    # 获取数值型变量字段的列表
    numerical_column_name = []
    for key_numerical_attribute_type in numerical_attribute_type.keys():
        numerical_column_name = numerical_column_name + numerical_attribute_type[key_numerical_attribute_type]
    numerical_column_name.remove("磁性")
    # 按照主键选取各项的范围
    key_name = process_data.loc[:, key_column]  # 获取数据主键的所有名称并去重
    key_name = key_name.drop_duplicates().tolist()
    processed_frame_data = pd.DataFrame()
    for i in range(len(key_name)):
        key_data_range = {}
        key_data = process_data[process_data[key_column].isin([key_name[i]])]
        key_data_range[key_column] = [key_name[i]]
        for j in range(len(columns_name)):
            if columns_name[j] not in ignored_column:
                data_columns = key_data[columns_name[j]].tolist()
                k = 0
                while k < len(data_columns):
                    if data_columns[k] != data_columns[k]:  # nan类型的数据与自己不相等
                        data_columns.pop(k)
                        k = k - 1
                    k = k + 1
                data_columns = list(set(data_columns))
                if len(data_columns) > 0:
                    # 判定数据的格式：文本型数据或数值型数据
                    if columns_name[j] in numerical_column_name:
                        data_type = "numerical"
                    else:
                        data_type = "document"

                    # 处理文本型数据和数值型数据
                    if data_type == "document":
                        if columns_name[j] == "表观形貌(球状、板状、粗糙、光滑、团聚、分散)":
                            k = 0
                            while k < len(data_columns):
                                if speech_analysis_positive_negative(data_columns[k], negativeWords) is False:
                                    data_columns.pop(k)
                                    k = k - 1
                                k = k + 1
                        if len(data_columns) == 1:
                            key_data_range[columns_name[j]] = data_columns
                        elif len(data_columns) > 1:
                            data_columns = ';'.join(data_columns)
                            key_data_range[columns_name[j]] = [data_columns]
                    elif data_type == "numerical":
                        if len(data_columns) >= 1:
                            k = 0
                            while k < len(data_columns):
                                if type(data_columns[k]) == str:
                                    data_columns[k] = "".join(filter(lambda c: c.isdigit() or c == "." or c == "-" or c == "~", data_columns[k]))
                                    if type(data_columns[k]) == str and "-" in data_columns[k]:
                                        if data_columns[k].split("-")[0] != "":
                                            data_columns.append(data_columns[k].split("-")[0])
                                        if data_columns[k].split("-")[1] != "":
                                            data_columns.append(data_columns[k].split("-")[1])
                                        data_columns.pop(k)
                                        k = k - 1
                                    if type(data_columns[k]) == str and "~" in data_columns[k]:
                                        if data_columns[k].split("~")[0] != "":
                                            data_columns.append(data_columns[k].split("~")[0])
                                        if data_columns[k].split("~")[1] != "":
                                            data_columns.append(data_columns[k].split("~")[1])
                                        data_columns.pop(k)
                                        k = k - 1
                                if data_columns[k] == "":  # 若字符串为空串则删除
                                    data_columns.pop(k)
                                    k = k - 1
                                k = k + 1
                        data_columns = map(float, data_columns)
                        data_columns = list(data_columns)
                        if len(data_columns) > 1:
                            data_columns.sort()
                            data_columns = [data_columns[0], data_columns[-1]]
                        key_data_range[columns_name[j]] = data_columns
                else:
                    key_data_range[columns_name[j]] = []

        frame_data = {}
        for key_name_range in key_data_range.keys():
            if len(key_data_range[key_name_range]) > 0:
                if key_name_range in numerical_column_name:
                    if len(key_data_range[key_name_range]) == 1:
                        frame_data[key_name_range] = key_data_range[key_name_range]
                    else:
                        frame_data[key_name_range] = str(key_data_range[key_name_range][0]) + "~" + str(key_data_range[key_name_range][-1])
                else:
                    frame_data[key_name_range] = key_data_range[key_name_range][0]
            else:
                if key_name_range in numerical_column_name:
                    frame_data[key_name_range] = ""
                else:
                    frame_data[key_name_range] = ""
        processed_frame_data = pd.concat([processed_frame_data, pd.DataFrame(frame_data, index=[i], columns=list(frame_data.keys()))])

    return processed_frame_data


def process(sheet_path, sheet_name, out_path):
    """
    函数名称：processing
    函数功能：处理表格的数据，将处理后的数据导出。
    参数1：sheet_path表示原表格的路径。
    参数2：sheet_name表示原表格的名称。
    参数3：out_path表示导出的路径。
    """
    original_data = pd.read_excel(sheet_path, sheet_name=sheet_name)
    [attribute_index, attribute_type] = process_extracting_data(original_data, keyAttribute, ignoredAttribute, attributeRange)
    sorted_Data = process_processing_data(original_data, keyAttribute, ignoredAttribute, attribute_index, attribute_type)
    sorted_Data.to_excel(out_path, index=False)

    return


def match_extracting_data(data, key_column, ignored_column, column_range):
    """
    函数名称：match_extracting_data
    函数功能：提取数据库中的信息。
    参数1：data表示原始数据库。
    参数2：key_column表示原始数据库的主键。
    参数3：ignored_column表示原始数据库中可以忽略字段名称的列表。
    参数4：column_range表示原始数据库中字段类型的字典。
    返回值：numerical_attribute_type表示数值型数据对应父字段包含内容的字典。
    """
    ignored_column.append(key_column)
    new_data = pd.DataFrame(data)
    columns_name = new_data.columns.tolist()
    # 获取数值型字段的名称
    numerical_attribute_type = {}
    for key_field_name in column_range.keys():
        key_index_first = columns_name.index(column_range[key_field_name][0])
        key_index_last = columns_name.index(column_range[key_field_name][1]) + 1
        result = columns_name[key_index_first:key_index_last]
        numerical_attribute_type[key_field_name] = result

    return numerical_attribute_type


def match_global_data(sorted_path, sorted_name):
    """
    函数名称：match_global_data
    函数功能：在函数内设置全局变量。
    参数1：sorted_path表示原表格的路径。
    参数2：sorted_name表示原表格的名称。
    """
    sorted_data = pd.read_excel(sorted_path, sheet_name=sorted_name)
    attribute_type = match_extracting_data(sorted_data, keyAttribute, ignoredAttribute, attributeRange)
    document_attribute = {
        "固态": ["废物类别", "行业分类", "物质组成特性", "物理形态(固态、半固态、液态)", "形状(块状、颗粒状、泥状、水状、粘稠状等)",
                 "表观形貌(球状、板状、粗糙、光滑、团聚、分散)", "颜色", "气味", "磁性"],
        "液态": ["废物类别", "行业分类", "物质组成特性", "物理形态(固态、半固态、液态)", "形状(块状、颗粒状、泥状、水状、粘稠状等)",
                 "表观形貌(球状、板状、粗糙、光滑、团聚、分散)", "颜色", "气味"],
        "半固态": ["废物类别", "行业分类", "物质组成特性", "物理形态(固态、半固态、液态)", "形状(块状、颗粒状、泥状、水状、粘稠状等)",
                   "表观形貌(球状、板状、粗糙、光滑、团聚、分散)", "颜色", "气味", "磁性"]}
    numerical_attribute = {
        "固态": attribute_type["其他数值特征"] + attribute_type["工业分析"] + attribute_type["元素组成"] + attribute_type["物相组成"] +
        attribute_type["污染物含量"] + attribute_type["有机污染物"] + attribute_type["毒性浸出浓度"],
        "液态": attribute_type["其他数值特征"] + attribute_type["元素组成"] + attribute_type["污染物含量"] + attribute_type["有机污染物"],
        "半固态": attribute_type["其他数值特征"] + attribute_type["工业分析"] + attribute_type["元素组成"] + attribute_type["物相组成"] +
        attribute_type["污染物含量"] + attribute_type["有机污染物"] + attribute_type["毒性浸出浓度"],
        "绝对数值": attribute_type["其他数值特征"] + attribute_type["工业分析"] + attribute_type["元素组成"] + attribute_type["物相组成"] +
        attribute_type["污染物含量"] + attribute_type["多环芳烃"] + attribute_type["毒性浸出浓度"],
        "二值化数值": attribute_type["有机污染物"]
    }
    grade_attribute = {
        "第一级": ["物理形态(固态、半固态、液态)", "形状(块状、颗粒状、泥状、水状、粘稠状等)", "表观形貌(球状、板状、粗糙、光滑、团聚、分散)", "颜色", "气味"],
        "第二级": attribute_type["其他数值特征"] + attribute_type["工业分析"],
        "第三级": attribute_type["元素组成"] + attribute_type["物相组成"] + attribute_type["污染物含量"] + attribute_type["多环芳烃"] + attribute_type["毒性浸出浓度"]
    }

    return [document_attribute, numerical_attribute, grade_attribute]


def match_matching_data(searching_dict, weight):
    """
    函数名称：match_matching_data
    函数功能：使用文本描述法或数值描述法综合搜索符合的数据。
    参数1：searching_dict表示搜索信息的字典。
    参数2：weight表示每项数据的权重。
    返回值：样本的名称列表、样本的匹配度列表。
    """
    index_matching = np.arange(sortedData.shape[0]).reshape(sortedData.shape[0], 1)
    index_matching_add = np.zeros(shape=(sortedData.shape[0], 1))
    index_matching = np.c_[index_matching, index_matching_add]
    attribute_name = list(searching_dict.keys())
    search_text = list(searching_dict.values())
    result_intersect_index = []
    if coreFeature["material_form"] not in attribute_name:
        error = "没有输入物理形态！"
        error_index = 0
        return [error, error_index]
    material_form_search = searching_dict[coreFeature["material_form"]]

    for i in range(index_matching.shape[0]):
        error_num = 0
        for j in range(len(attribute_name)):
            if attribute_name[j] in documentAttribute[material_form_search]:
                result_search_matching = document_search(attribute_name[j], search_text[j], i)
            elif attribute_name[j] in numericalAttribute[material_form_search]:
                result_search_matching = numerical_search(attribute_name[j], search_text[j], i)
                a = 1
            else:
                error = "输入了错误信息！"
                error_index = 1
                return [error, error_index]

            if result_search_matching > 0:
                if attribute_name[j] in gradeAttribute["第一级"]:
                    result_search_matching = result_search_matching * weight[0]
                elif attribute_name[j] in gradeAttribute["第二级"]:
                    result_search_matching = result_search_matching * weight[1]
                elif attribute_name[j] in gradeAttribute["第三级"]:
                    result_search_matching = result_search_matching * weight[2]
            else:
                error_num = error_num + 1

            if error_num <= 3:
                index_matching[i, 1] = index_matching[i, 1] + result_search_matching
            else:
                index_matching[i, 1] = 0.0
                break

    index_matching = index_matching[np.argsort(index_matching[:, 1])]
    index_matching = index_matching[::-1, :]
    zero_result = []
    for i in range(index_matching.shape[0]):
        if index_matching[i, 1] == 0:
            zero_result.append(i)
    index_matching = np.delete(index_matching, zero_result, axis=0)
    result_index = index_matching[:, 0].tolist()
    result_index = list(map(int, result_index))
    result_matching = index_matching[:, 1].tolist()
    result_name = sortedData.iloc[result_index, 0].tolist()

    return [result_name, result_matching]


def Matching(allDict):
    # 表格数据的主键与分类
    global keyAttribute
    global ignoredAttribute
    global attributeRange
    global negativeWords
    global sortedData
    global coreFeature
    global documentAttribute
    global numericalAttribute
    global gradeAttribute
    keyAttribute = "固废名称"
    ignoredAttribute = ["数据来源", "废物描述", "表观形貌(稍微详细)", "特征指标", "产生工段"]
    attributeRange = {"其他数值特征": ["含水率(%)", "COD(mg/L)"], "工业分析": ["挥发分含量", "硫分含量"],
                      "元素组成": ["C", "Po"], "物相组成": ["B2O3", "氯化铵"], "污染物含量": ["T B", "无机氟化物(不包括氟化钙)"],
                      "多环芳烃": ["萘", "苯并(ghi)北(二萘嵌苯)"], "有机污染物": ["乙酸乙酯", "咪鲜胺"], "毒性浸出浓度": ["L Ca", "L V"]}
    negativeWords = ["没有", "无"]
    # # 提取并导出表格数据
    # sheetPath = r"E:\Peking University\实验室\2022.8 固废处理小程序\六行业汇总-10.18.xlsx"
    # sheetName = "六行业汇总-10.18"
    # outPath = r"E:\Peking University\实验室\2022.8 固废处理小程序\六行业汇总-10.18-处理后.xlsx"
    # process(sheetPath, sheetName, outPath)
    # 读取的表格数据
    sortedPath = r"C:\Users\14213\Desktop\python\waste\wasteSearch\files\六行业汇总-10.18-处理后.xlsx"
    sortedName = "Sheet1"
    sortedData = pd.read_excel(sortedPath, sheet_name=sortedName)
    # sortedData = WasteInfo.objects.filter(dataId__gte=999)
    # 字段的全局信息
    coreFeature = {"material_form": "物理形态(固态、半固态、液态)", "material_appearance": "表观形貌(球状、板状、粗糙、光滑、团聚、分散)",
                   "water_content": "含水率(%)"}
    [documentAttribute, numericalAttribute, gradeAttribute] = match_global_data(sortedPath, sortedName)

    # 文本识别
    attributeWeight = [3, 2, 1]
    # allDict = {"物理形态(固态、半固态、液态)": "固态", "表观形貌(球状、板状、粗糙、光滑、团聚、分散)": "板状、光滑", "含水率(%)": 4,
            #    "行业分类": "有色冶炼", "形状(块状、颗粒状、泥状、水状、粘稠状等)": "泥状", "颜色": "黑色", "Zn": 10, "Pb": 8}
    [resultName, resultMatching] = match_matching_data(allDict, attributeWeight)

    res = []
    for name, value in zip(resultName, resultMatching):
        if value > 0:
            res.append(name)
    
    # print(res)
    return(res)

    # print(resultName)
    # print(resultMatching)
